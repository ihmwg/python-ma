"""Representation of an IHM mmCIF file as a set of Python classes.

   Generally class names correspond to mmCIF table names and class
   attributes to mmCIF attributes (with prefixes like `pdbx_` stripped).
   For example, the data item _entity.details is found in the
   :class:`Entity` class, as the `details` member.

   Ordinals and IDs are generally not used in this representation (instead,
   pointers to objects are used).
"""

import itertools
from .format import CifWriter
import sys
# Handle different naming of urllib in Python 2/3
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json

#: A value that isn't known. Note that this is distinct from a value that
#: is deliberately omitted, which is represented by Python None.
unknown = CifWriter.unknown

def _remove_identical(gen):
    """Return only unique objects from `gen`.
       Objects that are identical are only returned once, although multiple
       non-identical objects that compare equal may be returned."""
    seen_objs = {}
    for obj in gen:
        if id(obj) in seen_objs:
            continue
        seen_objs[id(obj)] = None
        yield obj

class System(object):
    """Top-level class representing a complete modeled system.

       :param str title: Title (longer text description) of the system.
       :param str id: Unique identifier for this system in the mmCIF file.
    """

    def __init__(self, title=None, id='model'):
        self.id = id
        self.title = title

        #: List of plain text comments. These will be added to the top of
        #: the mmCIF file.
        self.comments = []

        #: List of all software used in the modeling. See :class:`Software`.
        self.software = []

        #: List of all citations. See :class:`Citation`.
        self.citations = []

        #: All entities used in the system. See :class:`Entity`.
        self.entities = []

        #: All asymmetric units used in the system. See :class:`AsymUnit`.
        self.asym_units = []

        #: All orphaned assemblies in the system. See :class:`Assembly`.
        #: This can be used to keep track of all assemblies that are not
        #: otherwise used - normally one is assigned to a
        #: :class:`~ihm.model.Model`,
        #: :class:`ihm.protocol.Step`, or
        #: :class:`~ihm.restraint.Restraint`.
        self.orphan_assemblies = []

        #: The assembly of the entire system. By convention this is always
        #: the first assembly in the mmCIF file (assembly_id=1). Note that
        #: currently this isn't filled in on output until dumper.write()
        #: is called. See :class:`Assembly`
        self.complete_assembly = Assembly((), name='Complete assembly',
                                          description='All known components')

        #: Locations of all extra resources.
        #: See :class:`~ihm.location.Location`.
        self.locations = []

        #: All orphaned datasets.
        #: This can be used to keep track of all datasets that are not
        #: otherwise used - normally a dataset is assigned to a
        #: :class:`~ihm.dataset.DatasetGroup`,
        #: :class:`~ihm.startmodel.StartingModel`,
        #: :class:`~ihm.restraint.Restraint`,
        #: :class:`~ihm.startmodel.Template`,
        #: or as the parent of another :class:`~ihm.dataset.Dataset`.
        #: See :class:`~ihm.dataset.Dataset`.
        self.orphan_datasets = []

        #: All orphaned groups of datasets.
        #: This can be used to keep track of all dataset groups that are not
        #: otherwise used - normally a group is assigned to a
        #: :class:`~ihm.protocol.Protocol`.
        #: See :class:`~ihm.dataset.DatasetGroup`.
        self.orphan_dataset_groups = []

        #: All orphaned representations of the system.
        #: This can be used to keep track of all representations that are not
        #: otherwise used - normally one is assigned to a
        #: :class:`~ihm.model.Model`.
        #: See :class:`~ihm.representation.Representation`.
        self.orphan_representations = []

        #: All orphaned starting models for the system.
        #: This can be used to keep track of all starting models that are not
        #: otherwise used - normally one is assigned to an
        #: :class:`ihm.representation.Segment`.
        #: See :class:`~ihm.startmodel.StartingModel`.
        self.orphan_starting_models = []

        #: All restraints on the system.
        #: See :class:`~ihm.restraint.Restraint`.
        self.restraints = []

        #: All orphaned modeling protocols.
        #: This can be used to keep track of all protocols that are not
        #: otherwise used - normally a protocol is assigned to a
        #: :class:`~ihm.model.Model`.
        #: See :class:`~ihm.protocol.Protocol`.
        self.orphan_protocols = []

        #: All ensembles.
        #: See :class:`~ihm.model.Ensemble`.
        self.ensembles = []

        #: All state groups (collections of models).
        #: See :class:`~ihm.model.StateGroup`.
        self.state_groups = []

    def update_locations_in_repositories(self, repos):
        """Update all :class:`Location` objects in the system that lie within
           a checked-out :class:`Repository` to point to that repository.

           This is intended for the use case where the current working directory
           is a checkout of a repository which is archived somewhere with a DOI.
           Locations can then be simply constructed pointing to local files,
           and retroactively updated with this method to point to the DOI if
           appropriate.

           For each Location, if it points to a local file that is below the
           `root` of one of the `repos`, update it to point to that repository.
           If is under multiple roots, pick the one that gives the shortest
           path. For example, if run in a subdirectory `foo` of a repository
           archived as `repo.zip`, the local path `simple.pdb` will
           be updated to be `repo-top/foo/simple.pdb` in `repo.zip`::

               l = ihm.location.InputFileLocation("simple.pdb")
               system.locations.append(l)

               r = ihm.location.Repository(doi='1.2.3.4',
                         url='https://example.com/repo.zip',)
                         top_directory="repo-top", root="..")
               system.update_locations_in_repositories([r])
        """
        for loc in self._all_locations():
            if isinstance(loc, location.FileLocation):
                location.Repository._update_in_repos(loc, repos)

    def _all_model_groups(self):
        """Iterate over all ModelGroups in the system"""
        # todo: raise an error if a modelgroup is present in multiple states
        for state_group in self.state_groups:
            for state in state_group:
                for model_group in state:
                    yield model_group

    def _all_models(self):
        """Iterate over all Models in the system"""
        # todo: raise an error if a model is present in multiple groups
        for group in self._all_model_groups():
            seen_models = {}
            for model in group:
                if model in seen_models:
                    continue
                seen_models[model] = None
                yield group, model

    def _all_representations(self):
        """Iterate over all Representations in the system.
           This includes all Representations referenced from other objects, plus
           any orphaned Representations. Duplicates are filtered out."""
        return _remove_identical(itertools.chain(
                   self.orphan_representations,
                   (model.representation for group, model in self._all_models()
                                         if model.representation)))

    def _all_segments(self):
        for representation in self._all_representations():
            for segment in representation:
                yield segment

    def _all_starting_models(self):
        """Iterate over all StartingModels in the system.
           This includes all StartingModels referenced from other objects, plus
           any orphaned StartingModels. Duplicates are filtered out."""
        return _remove_identical(itertools.chain(
                   self.orphan_starting_models,
                   (segment.starting_model for segment in self._all_segments()
                                           if segment.starting_model)))

    def _all_protocols(self):
        """Iterate over all Protocols in the system.
           This includes all Protocols referenced from other objects, plus
           any orphaned Protocols. Duplicates are filtered out."""
        return _remove_identical(itertools.chain(
                        self.orphan_protocols,
                        (model.protocol for group, model in self._all_models()
                                        if model.protocol)))

    def _all_protocol_steps(self):
        for protocol in self._all_protocols():
            for step in protocol.steps:
                yield step

    def _all_analysis_steps(self):
        for protocol in self._all_protocols():
            for analysis in protocol.analyses:
                for step in analysis.steps:
                    yield step

    def _all_assemblies(self):
        """Iterate over all Assemblies in the system.
           This includes all Assemblies referenced from other objects, plus
           any orphaned Assemblies. Duplicates may be present."""
        return itertools.chain(
                        # Complete assembly is always first
                        (self.complete_assembly,),
                        self.orphan_assemblies,
                        (model.assembly for group, model in self._all_models()
                                        if model.assembly),
                        (step.assembly for step in self._all_protocol_steps()
                                       if step.assembly),
                        (step.assembly for step in self._all_analysis_steps()
                                       if step.assembly),
                        (restraint.assembly for restraint in self.restraints
                                            if restraint.assembly))

    def _all_dataset_groups(self):
        """Iterate over all DatasetGroups in the system.
           This includes all DatasetGroups referenced from other objects, plus
           any orphaned groups. Duplicates may be present."""
        return itertools.chain(
                  self.orphan_dataset_groups,
                  (step.dataset_group for step in self._all_protocol_steps()
                                      if step.dataset_group),
                  (step.dataset_group for step in self._all_analysis_steps()
                                      if step.dataset_group))

    def _all_templates(self):
        """Iterate over all Templates in the system."""
        for startmodel in self._all_starting_models():
            for template in startmodel.templates:
                yield template

    def _all_datasets_except_parents(self):
        """Iterate over all Datasets except those referenced only
           as the parent of another Dataset. Duplicates may be present."""
        def _all_datasets_in_groups():
            for dg in self._all_dataset_groups():
                for d in dg:
                    yield d
        return itertools.chain(
                  self.orphan_datasets,
                  _all_datasets_in_groups(),
                  (sm.dataset for sm in self._all_starting_models()
                              if sm.dataset),
                  (restraint.dataset for restraint in self.restraints
                                     if restraint.dataset),
                  (template.dataset for template in self._all_templates()
                                    if template.dataset))

    def _all_datasets(self):
        """Iterate over all Datasets in the system.
           This includes all Datasets referenced from other objects, plus
           any orphaned datasets. Duplicates may be present."""
        def _all_datasets_and_parents(d):
            for p in d.parents:
                for alld in _all_datasets_and_parents(p):
                    yield alld
            yield d
        for d in self._all_datasets_except_parents():
            for alld in _all_datasets_and_parents(d):
                yield alld

    def _all_locations(self):
        """Iterate over all Locations in the system.
           This includes all Locations referenced from other objects, plus
           any referenced from the top-level system.
           Duplicates may be present."""
        def all_densities():
            for ensemble in self.ensembles:
                for density in ensemble.densities:
                    yield density
        return itertools.chain(
                self.locations,
                (dataset.location for dataset in self._all_datasets()
                          if hasattr(dataset, 'location') and dataset.location),
                (ensemble.file for ensemble in self.ensembles if ensemble.file),
                (density.file for density in all_densities() if density.file),
                (template.alignment_file for template in self._all_templates()
                                         if template.alignment_file))

    def _all_citations(self):
        """Iterate over all Citations in the system.
           This includes all Citations referenced from other objects, plus
           any referenced from the top-level system.
           Duplicates are filtered out."""
        return _remove_identical(itertools.chain(
                        self.citations,
                        (restraint.fitting_method_citation_id
                            for restraint in self.restraints
                            if hasattr(restraint, 'fitting_method_citation_id')
                            and restraint.fitting_method_citation_id)))

    def _make_complete_assembly(self):
        """Fill in the complete assembly with all entities/asym units"""
        # Clear out any existing components
        self.complete_assembly[:] = []

        # Include all asym units
        seen_entities = {}
        for asym in self.asym_units:
            self.complete_assembly.append(asym)
            seen_entities[asym.entity] = None
        # Add all entities without structure
        for entity in self.entities:
            if entity not in seen_entities:
                self.complete_assembly.append(entity)


class Software(object):
    """Software used as part of the modeling protocol.

       :param str name: The name of the software.
       :param str classification: The major function of the sofware, for
              example 'model building', 'sample preparation', 'data collection'.
       :param str description: A longer text description of the software.
       :param str location: Place where the software can be found (e.g. URL).
       :param str type: Type of software (program/package/library/other).
       :param str version: The version used.

       See :attr:`System.software`."""
    def __init__(self, name, classification, description, location,
                 type='program', version=None):
        self.name = name
        self.classification = classification
        self.description = description
        self.location = location
        self.type = type
        self.version = version

    # Software compares equal if the names and versions are the same
    def _eq_vals(self):
        return (self.name, self.version)
    def __eq__(self, other):
        return self._eq_vals() == other._eq_vals()
    def __hash__(self):
        return hash(self._eq_vals())


class Citation(object):
    """A publication that describes the modeling.

       See :attr:`System.citations`.

       :param str pmid: The PubMed ID.
       :param str title: Full title of the publication.
       :param str journal: Abbreviated journal name.
       :param int volume: Journal volume number.
       :param page_range: The page (int) or page range (as a 2-element
              int tuple).
       :param int year: Year of publication.
       :param authors: All authors in order, as a list of strings (last name
              followed by initials, e.g. "Smith AJ").
       :param str doi: Digitial Object Identifier of the publication.
    """
    def __init__(self, pmid, title, journal, volume, page_range, year, authors,
                 doi):
        self.title, self.journal, self.volume = title, journal, volume
        self.page_range, self.year = page_range, year
        self.pmid, self.authors, self.doi = pmid, authors, doi

    @classmethod
    def from_pubmed_id(cls, pubmed_id):
        """Create a Citation from just a PubMed ID.
           This is done by querying NCBI's web api, so requires network access.

           :param int pubmed_id: The PubMed identifier.
           :return: A new Citation for the given identifier.
           :rtype: :class:`Citation`
        """
        def get_doi(ref):
            for art_id in ref['articleids']:
                if art_id['idtype'] == 'doi':
                    return enc(art_id['value'])
        # JSON values are always Unicode, but on Python 2 we want non-Unicode
        # strings, so convert to ASCII
        if sys.version_info[0] < 3:
            def enc(s):
                return s.encode('ascii')
        else:
            def enc(s):
                return s

        url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
               '?db=pubmed&retmode=json&rettype=abstract&id=%s' % pubmed_id)
        fh = urllib2.urlopen(url)
        j = json.load(fh)
        fh.close()
        ref = j['result'][str(pubmed_id)]
        authors = [enc(x['name']) for x in ref['authors'] \
                   if x['authtype'] == 'Author']

        return cls(pmid=pubmed_id, title=enc(ref['title']),
                   journal=enc(ref['source']), volume=enc(ref['volume']),
                   page_range=enc(ref['pages']).split('-'),
                   year=enc(ref['pubdate']).split()[0],
                   authors=authors, doi=get_doi(ref))


class ChemComp(object):
    """A chemical component from which :class:`Entity` objects are constructed.
       Usually these are amino acids (see :class:`LPeptideChemComp`) or
       nucleic acids (see :class:`DNAChemComp` and :class:`RNAChemComp`).

       For standard amino and nucleic acids, it is generally easier to use
       a :class:`Alphabet` and refer to the components with their one-letter
       (amino acids, RNA) or two-letter (DNA) codes.

       :param str id: A globally unique identifier for this component.
       :param str code: A shorter identifier (usually one letter) that only
              needs to be unique in the entity.
       :param str code_canonical: Canonical version of `code` (which need not
              be unique).

       For example, glycine would have
       ``id='GLY', code='G', code_canonical='G'`` while selenomethionine would
       use ``id='MSE', code='MSE', code_canonical='M'``, guanosine (RNA)
       ``id='G', code='G', code_canonical='G'``, and deoxyguanosine (DNA)
       ``id='DG', code='DG', code_canonical='G'``.
    """

    __slots__ = ['code', 'code_canonical', 'id', 'type']

    type = 'other'

    def __init__(self, id, code, code_canonical):
        self.id = id
        self.code, self.code_canonical = code, code_canonical

    # Equal if all identifiers are the same
    def __eq__(self, other):
        return ((self.code, self.code_canonical, self.id, self.type) ==
                (other.code, other.code_canonical, other.id, other.type))


class PeptideChemComp(ChemComp):
    """A single peptide component. Usually :class:`LPeptideChemComp` is used
       instead (except for glycine) to specify chirality.
       See :class:`ChemComp` for a description of the parameters."""
    type = 'Peptide linking'


class LPeptideChemComp(PeptideChemComp):
    """A single peptide component with L- chirality.
       See :class:`ChemComp` for a description of the parameters."""
    type = 'L-peptide linking'


class DNAChemComp(ChemComp):
    """A single DNA component.
       See :class:`ChemComp` for a description of the parameters."""
    type = 'DNA linking'


class RNAChemComp(ChemComp):
    """A single RNA component.
       See :class:`ChemComp` for a description of the parameters."""
    type = 'RNA linking'


def _pep_comp_class(one_letter):
    return PeptideChemComp if one_letter == 'G' else LPeptideChemComp

class Alphabet(object):
    """A mapping from codes (usually one-letter, or two-letter for DNA) to
       chemical components.
       These classes can be used to construct sequences of components
       when creating an :class:`Entity`. It is generally not necessary to
       instantiate these objects.
       See :class:`LPeptideAlphabet`, :class:`RNAAlphabet`,
       :class:`DNAAlphabet`.
    """
    pass


class LPeptideAlphabet(Alphabet):
    """A mapping from one-letter amino acid codes (e.g. H, M) to
       L-amino acids (as :class:`LPeptideChemComp` objects, except for achiral
       glycine which maps to :class:`PeptideChemComp`). Some other common
       modified residues are also included (e.g. MSE). For these their full name
       rather than a one-letter code is used.
    """
    _comps = dict([code, _pep_comp_class(code)(id, code, code)] for code, id in
                    [('A', 'ALA'), ('C', 'CYS'), ('D', 'ASP'), ('E', 'GLU'),
                     ('F', 'PHE'), ('G', 'GLY'), ('H', 'HIS'), ('I', 'ILE'),
                     ('K', 'LYS'), ('L', 'LEU'), ('M', 'MET'), ('N', 'ASN'),
                     ('P', 'PRO'), ('Q', 'GLN'), ('R', 'ARG'), ('S', 'SER'),
                     ('T', 'THR'), ('V', 'VAL'), ('W', 'TRP'), ('Y', 'TYR')])

    # common non-standard L-amino acids
    _comps.update([id, LPeptideChemComp(id, id, canon)] for id, canon in
                     [('MSE', 'M')])


class RNAAlphabet(Alphabet):
    """A mapping from one-letter nucleic acid codes (e.g. A) to
       RNA (as :class:`RNAChemComp` objects)."""
    _comps = dict([id, RNAChemComp(id, id, id)] for id in 'ACGU')


class DNAAlphabet(Alphabet):
    """A mapping from two-letter nucleic acid codes (e.g. DA) to
       DNA (as :class:`DNAChemComp` objects)."""
    _comps = dict([code, DNAChemComp(code, code, canon)] for code, canon in
                    [('DA', 'A'), ('DC', 'C'), ('DG', 'G'), ('DT', 'T')])


class EntityRange(object):
    """Part of an entity. Usually these objects are created from
       an :class:`Entity`, e.g. to get a range covering residues 4 through
       7 in `entity` use::

           entity = ihm.Entity(seq=...)
           rng = entity(4,7)
    """
    def __init__(self, entity, seq_id_begin, seq_id_end):
        self.entity = entity
        # todo: check range for validity (at property read time)
        self.seq_id_range = (seq_id_begin, seq_id_end)

    def __eq__(self, other):
        try:
            return (self.entity is other.entity
                    and self.seq_id_range == other.seq_id_range)
        except AttributeError:
            return False
    def __hash__(self):
        return hash((id(self.entity), self.seq_id_range))

    # Use same ID as the original entity
    _id = property(lambda self: self.entity._id)


class Residue(object):
    """A single residue in an entity or asymmetric unit. Usually these objects
       are created by calling :meth:`Entity.residue` or
       :meth:`AsymUnit.residue`.
    """
    def __init__(self, seq_id, entity=None, asym=None):
        self.entity = entity
        self.asym = asym
        # todo: check id for validity (at property read time)
        self.seq_id = seq_id


class Entity(object):
    """Represent a CIF entity (with a unique sequence)

       :param str seq: The primary sequence as a string of one-letter
              amino acid codes.
       :param str description: A short text name for the sequence.
       :param str details: Longer text describing the sequence.

       See :attr:`System.entities`.

       Note that currently only standard amino acids are supported.
    """

    type = 'polymer'
    src_method = 'man'
    number_of_molecules = 1
    formula_weight = unknown

    def __init__(self, seq, description=None, details=None):
        self.sequence = seq
        self.description, self.details = description, details

    def residue(self, seq_id):
        """Get a :class:`Residue` at the given sequence position"""
        return Residue(entity=self, seq_id=seq_id)

    # Entities are considered identical if they have the same sequence
    def __eq__(self, other):
        return self.sequence == other.sequence
    def __hash__(self):
        return hash(self.sequence)

    def __call__(self, seq_id_begin, seq_id_end):
        return EntityRange(self, seq_id_begin, seq_id_end)

    seq_id_range = property(lambda self: (1, len(self.sequence)),
                            doc="Sequence range")


class AsymUnitRange(object):
    """Part of an asymmetric unit. Usually these objects are created from
       an :class:`AsymUnit`, e.g. to get a range covering residues 4 through
       7 in `asym` use::

           asym = ihm.AsymUnit(entity)
           rng = asym(4,7)
    """
    def __init__(self, asym, seq_id_begin, seq_id_end):
        self.asym = asym
        # todo: check range for validity (at property read time)
        self.seq_id_range = (seq_id_begin, seq_id_end)

    def __eq__(self, other):
        try:
            return (self.asym is other.asym
                    and self.seq_id_range == other.seq_id_range)
        except AttributeError:
            return False
    def __hash__(self):
        return hash((id(self.asym), self.seq_id_range))

    # Use same ID and entity as the original asym unit
    _id = property(lambda self: self.asym._id)
    _ordinal = property(lambda self: self.asym._ordinal)
    entity = property(lambda self: self.asym.entity)


class AsymUnit(object):
    """An asymmetric unit, i.e. a unique instance of an Entity that
       was modeled.

       :param entity: The unique sequence of this asymmetric unit.
       :type entity: :class:`Entity`
       :param str details: Longer text description of this unit.

       See :attr:`System.asym_units`.
    """

    def __init__(self, entity, details=None):
        self.entity, self.details = entity, details

    def __call__(self, seq_id_begin, seq_id_end):
        return AsymUnitRange(self, seq_id_begin, seq_id_end)

    def residue(self, seq_id):
        """Get a :class:`Residue` at the given sequence position"""
        return Residue(asym=self, seq_id=seq_id)

    seq_id_range = property(lambda self: (1, len(self.entity.sequence)),
                            doc="Sequence range")


class Assembly(list):
    """A collection of parts of the system that were modeled or probed
       together.

       :param sequence elements: Initial set of parts of the system.
       :param str name: Short text name of this assembly.
       :param str description: Longer text that describes this assembly.

       This is implemented as a simple list of asymmetric units (or parts of
       them) and/or entities (or parts of them), i.e. a list of
       :class:`AsymUnit`, :class:`AsymUnitRange`,
       :class:`Entity`, and :class:`EntityRange` objects. An Assembly is
       typically assigned to one or more of

         - :class:`~ihm.model.Model`
         - :class:`ihm.protocol.Step`
         - :class:`ihm.analysis.Step`
         - :class:`~ihm.restraint.Restraint`

       See also :attr:`System.complete_assembly`
       and :attr:`System.orphan_assemblies`.

       Note that any duplicate assemblies will be pruned on output."""

    #: :class:`Assembly` that is the immediate parent in a hierarchy, or `None`
    parent = None

    def __init__(self, elements=(), name=None, description=None):
        super(Assembly, self).__init__(elements)
        self.name, self.description = name, description
