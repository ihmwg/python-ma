"""Classes for linking back to a sequence or structure database."""


class TargetReference(object):
    """Point to the sequence of a target :class:`modelcif.Entity` in a sequence
       database. Typically a subclass such as :class:`UniProt` is used,
       although to use a custom database, make a new subclass and provide
       a docstring to describe the database, e.g.::

           class CustomRef(TargetReference):
               "my custom database"

       :param str code: The name of the sequence in the database.
       :param str accession: The database accession.
       :param int align_begin: Beginning index of the sequence in the database.
              If omitted, it will be assumed that the Entity corresponds to
              the full database sequence.
       :param int align_end: Ending index of the sequence in the database.
              If omitted, it will be assumed that the Entity corresponds to
              the full database sequence.
       :param str isoform: Sequence isoform, if applicable.
       :param str ncbi_taxonomy_id: Taxonomy identifier provided by NCBI.
       :param str organism_scientific: Scientific name of the organism.
    """

    name = 'Other'

    def __init__(self, code, accession, align_begin=None, align_end=None,
                 isoform=None, ncbi_taxonomy_id=None,
                 organism_scientific=None):
        self.code, self.accession = code, accession
        self.align_begin, self.align_end = align_begin, align_end
        self.isoform = isoform
        self.ncbi_taxonomy_id = ncbi_taxonomy_id
        self.organism_scientific = organism_scientific

    def _get_other_details(self):
        if (type(self) is not TargetReference
                and self.name == TargetReference.name):
            return self.__doc__.split('\n')[0]

    other_details = property(
        _get_other_details,
        doc="More information about a custom reference type. "
            "By default it is the first line of the docstring.")


class UniProt(TargetReference):
    """Point to the sequence of an :class:`modelcif.Entity` in UniProt.

       These objects are typically passed to the :class:`modelcif.Entity`
       constructor for target sequences (for templates, see
       :class:`TemplateReference`).

       See :class:`TargetReference` for a description of the parameters.
    """
    name = 'UNP'
    other_details = None


class TemplateReference(object):
    """Point to the structure of a :class:`modelcif.Template` in a structure
       database.

       These objects are typically passed to the :class:`modelcif.Template`
       constructor for template sequences (for target sequences, see
       :class:`Targeteference`).

       Typically a subclass such as :class:`PDB` is used,
       although to use a custom database, make a new subclass and provide
       a docstring to describe the database, e.g.::

           class CustomRef(TemplateReference):
               "my custom database"

       :param str accession: The database accession.
    """
    name = 'Other'

    def __init__(self, accession):
        self.accession = accession

    def _get_other_details(self):
        if (type(self) is not TemplateReference
                and self.name == TemplateReference.name):
            return self.__doc__.split('\n')[0]

    other_details = property(
        _get_other_details,
        doc="More information about a custom reference type. "
            "By default it is the first line of the docstring.")


class PDB(TemplateReference):
    """Point to the structure of a :class:`modelcif.Template` in PDB.

       These objects are typically passed to the :class:`modelcif.Template`
       constructor.

       See :class:`TemplateReference` for a description of the parameters.
    """
    name = 'PDB'
    other_details = None