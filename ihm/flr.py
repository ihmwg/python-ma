"""Classes to handle fluorescence data.
   The classes roughly correspond to categories in the
   [FLR dictionary](https://github.com/ihmwg/FLR-dictionary/).

   See the top level :class:`FLRData` class for more information.
"""

class Probe(object):
    """Defines a fluorescent probe.

       This class is not in the FLR dictionary, but it collects all the
       information connected by the probe_ids.

       :param probe_list_entry: A probe list object.
       :type probe_list_entry: :class:`ProbeList`
       :param probe_descriptor: A probe descriptor.
       :type probe_descriptor: :class:`ProbeDescriptor`
    """

    def __init__(self, probe_list_entry=None,probe_descriptor=None):
        self.probe_list_entry = probe_list_entry
        self.probe_descriptor = probe_descriptor

    ## Set the probe_list entry of the probe
    def add_probe_list_entry(self,probe_list_entry):
        self.probe_list_entry = probe_list_entry

    ## set the probe_descriptor of the probe
    def add_probe_descriptor(self,probe_descriptor):
        self.probe_descriptor = probe_descriptor

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ProbeDescriptor(object):
    """Collects the chemical descriptors for a fluorescent probe.

       This includes the chemical descriptor of the reactive probe and
       the chromophore.

       :param reactive_probe_chem_descriptor: The chemical descriptor for
              the reactive probe.
       :type reactive_probe_chem_descriptor: :class:`ihm.ChemDescriptor`
       :param chromophore_chem_descriptor: The chemical descriptor of the
              chromophore.
       :type chromophore_chem_descriptor: :class:`ihm.ChemDescriptor`
       :param chromophore_center_atom: The atom describing the center
              of the chromophore.
    """

    def __init__(self, reactive_probe_chem_descriptor,
                 chromophore_chem_descriptor, chromophore_center_atom=None):
        self.reactive_probe_chem_descriptor = reactive_probe_chem_descriptor
        self.chromophore_chem_descriptor = chromophore_chem_descriptor
        self.chromophore_center_atom = chromophore_center_atom

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ProbeList(object):
    """Store the chromophore name, whether there is a reactive probe
       available, the origin of the probe and the type of linkage of the probe.

       :param chromophore_name: The name of the chromophore.
       :param reactive_probe_flag: Flag to indicate whether a reactive
              probe is given.
       :param reactive_probe_name: The name of the reactive probe.
       :param probe_origin: The origin of the probe (intrinsic or extrinsic).
       :param probe_link_type: The type of linkage for the probe (covalent
              or ligand).
    """

    def __init__(self, chromophore_name, reactive_probe_flag=False,
                 reactive_probe_name=None, probe_origin=None,
                 probe_link_type=None):
        self.chromophore_name = chromophore_name
        self.reactive_probe_flag = reactive_probe_flag
        self.reactive_probe_name = reactive_probe_name
        self.probe_origin = probe_origin
        self.probe_link_type = probe_link_type

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SampleProbeDetails(object):
    """Connects a probe to a sample.

       :param sample: The sample.
       :type sample: :class:`Sample`
       :param probe: A probe that is attached to the sample.
       :type probe: :class:`Probe`
       :param fluorophore_type: The type of the fluorophore (donor,
              acceptor, or unspecified).
       :param poly_probe_position: The position on the polymer where
              the dye is attached to.
       :type poly_probe_position: :class:`PolyProbePosition`
       :param description: A description of the sample-probe-connection.
    """

    def __init__(self, sample, probe, fluorophore_type='unspecified',
                 poly_probe_position=None, description=None):
        self.sample = sample
        self.probe = probe
        self.fluorophore_type = fluorophore_type
        self.description = description
        self.poly_probe_position = poly_probe_position

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PolyProbeConjugate(object):
    """Describes the conjugate of polymer residue and probe (including
       possible linker)

       :param sample_probe: The :class:`SampleProbeDetails` object to
              which the conjugate is related.
       :type sample_probe: :class:`SampleProbeDetails`
       :param chem_descriptor: The chemical descriptor of the conjugate
              of polymer residue and probe.
       :type chem_descriptor: :class:`ihm.ChemDescriptor`
       :param ambiguous_stoichiometry: Flag whether the labeling is ambiguous.
       :param probe_stoichiometry: The stoichiometry of the ambiguous labeling.
    """

    def __init__(self, sample_probe, chem_descriptor,
                 ambiguous_stoichiometry=False, probe_stoichiometry=None):
        self.sample_probe = sample_probe
        self.chem_descriptor = chem_descriptor
        self.ambiguous_stoichiometry = ambiguous_stoichiometry
        self.probe_stoichiometry = probe_stoichiometry

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PolyProbePosition(object):
    """Describes a position on the polymer used for attaching the probe.

       This class combines Poly_probe_position, Poly_probe_position_modified,
       and Poly_probe_position_mutated from the FLR dictionary.

       :param entity: The entity the probe is attached to.
       :type entity: :class:`ihm.Entity`
       :param seq_id: The sequence number of the residue that was used
              to attach the probe.
       :param atom_id: The atom ID identifies the atom at which the probe
              was attached.
       :param comp_id: The chemical component id of the residue that was
              used to attach the probe.
       :param mutation_flag: Flag whether the residue was mutated
              (e.g. a Cys mutation).
       :param bool modification_flag: Flag whether the residue was modified
              (e.g. replacement of a residue with a labeled residue in
              case of nucleic acids).
       :param str auth_name: An author-given name for the position.
       :param mutated_chem_descriptor: The chemical descriptor of the
              mutated residue.
       :type mutated_chem_descriptor: :class:`ihm.ChemDescriptor`
       :param modified_chem_descriptor: The chemical descriptor of the
              modified residue.
       :type modified_chem_descriptor: :class:`ihm.ChemDescriptor`
    """

    def __init__(self, entity, seq_id, atom_id,
                 comp_id=None, mutation_flag=False, modification_flag=False,
                 auth_name=None, mutated_chem_descriptor=None,
                 modified_chem_descriptor=None):
        self.entity = entity
        self.seq_id = seq_id
        self.comp_id = comp_id
        ## The atom_id identifies the atom at which the probe is attached
        self.atom_id = atom_id
        self.mutation_flag = mutation_flag
        self.modification_flag = modification_flag
        self.auth_name = auth_name
        if self.mutation_flag:
            self.mutated_chem_descriptor = mutated_chem_descriptor
        if self.modification_flag:
            self.modified_chem_descriptor = modified_chem_descriptor

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Sample(object):
    """Sample corresponds to a measurement.

       :param entity_assembly: The assembly of the entities that was measured.
       :type entity_assembly: :class:`EntityAssembly`
       :param num_of_probes: The number of probes in the sample.
       :param sample_condition: The sample conditions for the Sample.
       :type sample_condition: :class:`SampleCondition`
       :param str sample_description: A description of the sample.
       :param str sample_details: Details about the sample.
       :param solvent_phase: The solvent phase of the sample (liquid,
              vitrified, or other).
    """

    def __init__(self, entity_assembly, num_of_probes, sample_condition,
                 sample_description=None, sample_details=None,
                 solvent_phase=None):
        self.entity_assembly = entity_assembly
        self.num_of_probes = num_of_probes
        self.sample_condition = sample_condition
        self.sample_description= sample_description
        self.sample_details = sample_details
        self.solvent_phase = solvent_phase

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class EntityAssembly(object):
    """The assembly of the entities that are in the system.

       :param entity: The entity to add.
       :type entity: :class:`Entity`
       :param num_copies: The number of copies for the entity in the assembly.
    """

    def __init__(self, entity=None, num_copies=0):
        self.entity_list = []
        self.num_copies_list = []
        if entity != None and num_copies != 0:
            self.add_entity(entity, num_copies)

    def add_entity(self, entity, num_copies):
        if num_copies < 0:
            raise ValueError("Number of copies for Entity must be "
                             "larger than zero.")
        self.entity_list.append(entity)
        self.num_copies_list.append(num_copies)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SampleCondition(object):
    """Description of the sample conditions.

       *Currently this is only text, but will be extended in the future.*

       :param str details: Description of the sample conditions.
    """

    def __init__(self, details=None):
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Experiment(object):
    """The Experiment collects combinations of instrument, experimental
       settings and sample.

       :param instrument: The instrument.
       :type instrument: :class:`Instrument`
       :param exp_setting: The experimental setting.
       :type exp_setting: :class:`ExpSetting`
       :param sample: The sample.
       :type sample: :class:`Sample`
       :param details: Details on the experiment.
    """

    def __init__(self, instrument=None, exp_setting=None, sample=None,
                 details=None):
        """The Experiment object can either be initiated with empty lists,
           or with an entry for each of them. In this way, an experiment
           object is created and filled with one entry.
        """
        self.instrument_list = []
        self.exp_setting_list = []
        self.sample_list = []
        self.details_list = []
        if instrument != None and exp_setting != None and sample != None:
            self.add_entry(instrument=instrument, exp_setting=exp_setting,
                           sample=sample, details=details)

    def add_entry(self, instrument, exp_setting, sample,details=None):
        """Entries to the experiment object can also be added one by one.
        """
        self.instrument_list.append(instrument)
        self.exp_setting_list.append(exp_setting)
        self.sample_list.append(sample)
        self.details_list.append(details)

    def get_entry_by_index(self, index):
        """Returns the combination of :class:`Instrument`, :class:`ExpSetting`,
           :class:`Sample`, and details for a given index.
        """
        return (self.instrument_list[index],
                self.exp_setting_list[index], self.sample_list[index],
                self.details_list[index])

    def __eq__(self, other):
#        return self.__dict__ == other.__dict__
        return ((self.instrument_list == other.instrument_list)
                and (self.exp_setting_list == other.exp_setting_list)
                and (self.sample_list == other.sample_list)
                and (self.details_list == other.details_list))

    def contains(self, instrument, exp_setting, sample):
        """Checks whether a combination of :class:`Instrument`,
           :class:`ExpSetting`, :class:`Sample` is already included in
           the experiment object.
        """
        ## TODO: possibly extend this by the details_list?
        for i in range(len(self.instrument_list)):
            if ((instrument == self.instrument_list[i])
                and (exp_setting == self.exp_setting_list[i])
                and (sample == self.sample_list[i])):
                return True
        return False


class Instrument(object):
    """Description of the Instrument used for the measurements.

       *Currently this is only text, but will be extended in the future.*

       :param details: Description of the instrument used for the measurements.
    """
    def __init__(self, details = None):
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ExpSetting(object):
    """Description of the experimental settings.

       *Currently this is only text, but will be extended in the future.*

       :param str details: Description of the experimental settings used for
              the measurement (e.g. temperature, or size of observation
              volume in case of confocal measurements).
    """

    def __init__(self, details = None):
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETAnalysis(object):
    """An analysis of FRET data that was performed.

       :param experiment: The Experiment object for this FRET analysis.
       :type experiment: :class:`Experiment`
       :param sample_probe_1: The combination of sample and probe for the
              first probe.
       :type sample_probe_1: :class:`SampleProbeDetails`
       :param sample_probe_2: The combination of sample and probe for the
              second probe.
       :type sample_probe_2: :class:`SampleProbeDetails`
       :param forster_radius: The Forster radius object for this FRET analysis.
       :type forster_radius: :class:`FRETForsterRadius`.
       :param calibration_parameters: The calibration parameters used for
              this analysis.
       :type calibration_parameters: :class:`FRETCalibrationParameters`
       :param method_name: The method used for the analysis.
       :param chi_square_reduced: The chi-square reduced as a quality
              measure for the fit.
       :param dataset: The dataset used.
       :type dataset: :class:`ihm.dataset.Dataset`
       :param external_file: The external file that contains (results of)
              the analysis.
       :param software: The software used for the analysis.
       :type software: :class:`ihm.Software`
    """

    def __init__(self, experiment, sample_probe_1, sample_probe_2,
                 forster_radius, calibration_parameters, method_name=None,
                 chi_square_reduced=None, dataset=None,
                 external_file=None, software=None):
        self.experiment = experiment
        self.sample_probe_1 = sample_probe_1
        self.sample_probe_2 = sample_probe_2
        self.forster_radius = forster_radius
        self.calibration_parameters = calibration_parameters
        self.method_name = method_name
        self.chi_square_reduced = chi_square_reduced
        self.dataset = dataset
        self.external_file = external_file
        self.software = software

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETDistanceRestraintGroup(object):
    """A collection of FRET distance restraints that are used together.
    """
    def __init__(self):
        self.distance_restraint_list = []

    def add_distance_restraint(self, distance_restraint):
        """Add a distance restraint to a distance_restraint_group"""
        self.distance_restraint_list.append(distance_restraint)

    def get_info(self):
        return self.distance_restraint_list

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETDistanceRestraint(object):
    """A distance restraint from FRET.

       :param sample_probe_1: The combination of sample and probe for
              the first probe.
       :type sample_probe_1: :class:`SampleProbeDetails`
       :param sample_probe_2: The combination of sample and probe for
              the second probe.
       :type sample_probe_2: :class:`SampleProbeDetails`
       :param analysis: The FRET analysis from which the distance
              restraint originated.
       :type analysis: :class:`FRETAnalysis`
       :param distance: The distance of the restraint.
       :param distance_error_plus: The (absolute, e.g. in Angstrom) error
              in the upper direction, such that
              ``upper boundary = distance + distance_error_plus``.
       :param distance_error_minus: The (absolute, e.g. in Angstrom) error
              in the lower direction, such that
              ``lower boundary = distance + distance_error_minus``.
       :param distance_type: The type of distance (<R_DA>, <R_DA>_E, or R_mp).
       :param state: The state the distance restraints is connected to.
              Important for multi-state models.
       :type state: :class:`ihm.model.State`
       :param population_fraction: The population fraction of the state
              in case of multi-state models.
       :param peak_assignment: The method how a peak was assigned.
       :type peak_assignment: :class:`PeakAssignment`
    """

    def __init__(self, sample_probe_1, sample_probe_2, analysis, distance,
                 distance_error_plus=0, distance_error_minus=0,
                 distance_type=None, state=None, population_fraction=0,
                 peak_assignment=None):
        self.sample_probe_1 = sample_probe_1
        self.sample_probe_2 = sample_probe_2
        self.state = state
        self.analysis = analysis
        self.distance = distance
        self.distance_error_plus = distance_error_plus
        self.distance_error_minus = distance_error_minus
        self.distance_type = distance_type
        self.population_fraction = population_fraction
        self.peak_assignment = peak_assignment

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETForsterRadius(object):
    """The FRET Forster radius between two probes.

       :param donor_probe: The donor probe.
       :type donor_probe: :class:`Probe`
       :param acceptor_probe: The acceptor probe.
       :type acceptor_probe: :class:`Probe`
       :param forster_radius: The Forster radius between the two probes.
       :param reduced_forster_radius: The reduced Forster radius between
              the two probes.
    """

    def __init__(self, donor_probe, acceptor_probe, forster_radius,
                 reduced_forster_radius=None):
        self.donor_probe = donor_probe
        self.acceptor_probe = acceptor_probe
        self.forster_radius = forster_radius
        self.reduced_forster_radius = reduced_forster_radius

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETCalibrationParameters(object):
    """The calibration parameter from the FRET measurements.
        For the definitions of the parameters see
        Hellenkamp et al. Nat. Methods 2018.

        :param phi_acceptor: The quantum yield of the acceptor.
        :param alpha: The alpha parameter.
        :param alpha_sd: The standard deviation of the alpha parameter.
        :param gG_gR_ratio: The ratio between of the green and red detection
               efficiencies.
        :param beta: The beta parameter.
        :param gamma: The gamma parameter.
        :param delta: The delta parameter.
        :param a_b: The fraction of bright molecules.
    """

    def __init__(self, phi_acceptor=None, alpha=None, alpha_sd=None,
                 gG_gR_ratio=None, beta=None, gamma=None, delta=None, a_b=None):
        self.phi_acceptor = phi_acceptor
        self.alpha = alpha
        self.alpha_sd = alpha_sd
        self.gG_gR_ratio = gG_gR_ratio
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.a_b = a_b

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PeakAssignment(object):
    """The method of peak assignment in case of multiple peaks,
        e.g. by population.

        :param method_name:
        :param details: The details of the peak assignment procedure.
    """
    def __init__(self, method_name, details=None):
        self.method_name = method_name
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETModelQuality(object):
    """The quality measure for a Model based on FRET data.

       :param model: The model being described.
       :type model: :class:`ihm.model.Model`
       :param chi_square_reduced: The quality of the model in terms of
              chi_square_reduced based on the Distance restraints used
              for the modeling.
       :param dataset_group: The group of datasets that was used for the
              quality estimation.
       :type dataset_group: :class:`ihm.dataset.DatasetGroup`
       :param method: The method used for judging the model quality.
       :param str details: Details on the model quality.
    """

    def __init__(self, model, chi_square_reduced, dataset_group,
                 method, details=None):
        self.model = model
        self.chi_square_reduced = chi_square_reduced
        self.dataset_group = dataset_group
        self.method = method
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FRETModelDistance(object):
    """The distance in a model for a certain distance restraint.

       :param restraint: The Distance restraint.
       :type restraint: :class:`FRETDistanceRestraint`
       :param model: The model the distance applies to.
       :type model: :class:`ihm.model.Model`
       :param distance: The distance obtained for the distance restraint
              in the current model.
       :param distance_deviation: The deviation of the distance in the
              model compared to the value of the distance restraint.
    """

    def __init__(self, restraint, model, distance,
                 distance_deviation=None):
        self.restraint = restraint
        self.model = model
        self.distance = distance
        self.distance_deviation = distance_deviation
        if self.distance_deviation is None and self.restraint is not None:
            self.calculate_deviation()

    def calculate_deviation(self):
        if self.distance_deviation is None and self.restraint is not None:
            self.distance_deviation = \
                       float(self.restraint.distance) - float(self.distance)

    def update_deviation(self):
        if self.restraint is not None:
            self.distance_deviation = \
                       float(self.restraint.distance) - float(self.distance)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ModelingCollection(object):
    """Not part of the flr dictionary.

       *In case of FPS, flr_modeling_list contains entries of FPSAVModeling
       or FPSMPPModeling and flr_modeling_method_list contains "FPS_AV"
       or "FPS_MPP"*
    """

    def __init__(self):
        self.flr_modeling_list = []
        self.flr_modeling_method_list = []

    def add_modeling(self, modeling, modeling_method):
        """ Modeling method can be "FPS_AV" or "FPS_MPP"
        """
        self.flr_modeling_list.append(modeling)
        self.flr_modeling_method_list.append(modeling_method)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSModeling(object):
    """Collect the modeling parameters for different steps of FPS,
       e.g. Docking, Refinement, or Error estimation.
       Members of this class automatically get assigned an id.

       :param protocol: The modeling protocol to which the FPS modeling
              step belongs.
       :type protocol: :class:`ihm.protocol.Protocol`
       :param restraint_group: The restraint group used for the modeling.
       :param global_parameter: The global FPS parameters used.
       :type global_parameter: :class:`FPSGlobalParameters`
       :param str probe_modeling_method: either "AV" or "MPP".
       :param str details: Details on the FPS modeling.
    """

    def __init__(self, protocol, restraint_group,
                 global_parameter, probe_modeling_method, details=None):
        self.protocol = protocol
        self.restraint_group = restraint_group
        self.global_parameter = global_parameter
        self.probe_modeling_method = probe_modeling_method
        self.details = details

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSGlobalParameters(object):
    """The global parameters in the FPS program.

       *For a description of the parameters, see also the FPS manual.*

       :param forster_radius: The Forster radius used in the FPS program.
       :param conversion_function_polynom_order: Order of the polynom for
              the conversion function between Rmp and <RDA>E.
       :param repetition: The number of repetitions.
       :param AV_grid_rel: The AV grid spacing relative to the smallest
              dye or linker dimension.
       :param AV_min_grid_A: The minimal AV grid spacing in Angstrom.
       :param AV_allowed_sphere: The allowed sphere radius.
       :param AV_search_nodes: Number of neighboring positions to be
              scanned for clashes.
       :param AV_E_samples_k: The number of samples for calculation
              of E (in thousand).
       :param sim_viscosity_adjustment: Daming rate during docking
              and refinement.
       :param sim_dt_adjustment: Time step during simulation.
       :param sim_max_iter_k: Maximal number of iterations (in thousand).
       :param sim_max_force: Maximal force.
       :param sim_clash_tolerance_A: Clash tolerance in Angstrom.
       :param sim_reciprocal_kT: reciprocal kT.
       :param sim_clash_potential: The clash potential.
       :param convergence_E: Convergence criterion E.
       :param convergence_K: Convergence criterion K.
       :param convergence_F: Convergence criterion F.
       :param convergence_T: Convergence criterion T.
       :param optimized_distances: Which distances are optimized?

    """
    def __init__(self, forster_radius, conversion_function_polynom_order,
                 repetition, AV_grid_rel, AV_min_grid_A, AV_allowed_sphere,
                 AV_search_nodes, AV_E_samples_k, sim_viscosity_adjustment,
                 sim_dt_adjustment, sim_max_iter_k, sim_max_force,
                 sim_clash_tolerance_A, sim_reciprocal_kT, sim_clash_potential,
                 convergence_E, convergence_K, convergence_F, convergence_T,
                 optimized_distances='All'):
        self.forster_radius = forster_radius
        self.conversion_function_polynom_order \
                = conversion_function_polynom_order
        self.repetition = repetition
        self.AV_grid_rel = AV_grid_rel
        self.AV_min_grid_A = AV_min_grid_A
        self.AV_allowed_sphere = AV_allowed_sphere
        self.AV_search_nodes = AV_search_nodes
        self.AV_E_samples_k = AV_E_samples_k
        self.sim_viscosity_adjustment = sim_viscosity_adjustment
        self.sim_dt_adjustment = sim_dt_adjustment
        self.sim_max_iter_k = sim_max_iter_k
        self.sim_max_force = sim_max_force
        self.sim_clash_tolerance_A = sim_clash_tolerance_A
        self.sim_reciprocal_kT = sim_reciprocal_kT
        self.sim_clash_potential = sim_clash_potential
        self.convergence_E = convergence_E
        self.convergence_K = convergence_K
        self.convergence_F = convergence_F
        self.convergence_T = convergence_T
        self.optimized_distances = optimized_distances

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSAVModeling(object):
    """FPS modeling using AV.
       This object connects the FPS_modeling step, the sample_probe and
       the respective AV parameters.

       :param fps_modeling: The FPS modeling ID.
       :type fps_modeling: :class:`FPSModeling`
       :param sample_probe: The Sample probe ID.
       :type sample_probe: :class:`SampleProbeDetails`
       :param parameter: The FPS AV parameters used.
       :type parameter: :class:`FPSAVParameter`
    """

    def __init__(self, fps_modeling, sample_probe, parameter):
        # fps_modeling is the object containing information on the
        # ihm modeling protocol, the restraint group and the global
        # FPS parameters
        self.fps_modeling = fps_modeling
        self.sample_probe = sample_probe
        self.parameter = parameter

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSAVParameter(object):
    """The AV parameters used for the modeling using FPS.

       :param num_linker_atoms: The number of atoms in the linker.
       :param linker_length: The length of the linker in Angstrom.
       :param linker_width: The width of the linker in Angstrom.
       :param probe_radius_1: The first radius of the probe.
       :param probe_radius_2: If AV3 is used, the second radius of the probe.
       :param probe_radius_3: If AV3 is used, the third radius of the probe.
    """

    def __init__(self, num_linker_atoms, linker_length, linker_width,
                 probe_radius_1, probe_radius_2=None, probe_radius_3=None):
        self.num_linker_atoms = num_linker_atoms
        self.linker_length = linker_length
        self.linker_width = linker_width
        self.probe_radius_1 = probe_radius_1
        self.probe_radius_2 = probe_radius_2
        self.probe_radius_3 = probe_radius_3

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSMPPModeling(object):
    """Maps the FPSModeling object to a mean probe position and connects it
       to the reference coordinate system.

       :param fps_modeling: The FPS modeling object.
       :type fps_modeling: :class:`FPSModeling`
       :param mpp: The ID of the mean probe position.
       :type mpp: :class:`FPSMeanProbePosition`
       :param mpp_atom_position_group:
       :type mpp_atom_position_group: :class:`FPSMPPAtomPositionGroup`
    """

    def __init__(self, fps_modeling, mpp, mpp_atom_position_group):
        # fps_modeling is the object containing information on the
        # ihm modeling protocol, the restraint group and the global
        # FPS parameters
        self.fps_modeling = fps_modeling
        self.mpp = mpp
        self.mpp_atom_position_group = mpp_atom_position_group

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSMeanProbePosition(object):
    """The mean probe position of an AV, which can be used instead of an AV.

       *It is usually not recommended to use this. Use AVs instead.*
       The coordinates are with respect to a reference coordinate system
       defined by :class:`FPSMPPAtomPositionGroup`.

       :param sample_probe: The Sample probe.
       :type sample_probe: :class:`SampleProbeDetails`
       :param mpp_xcoord: The x-coordinate of the mean probe position.
       :param mpp_ycoord: The y-coordinate of the mean probe position.
       :param mpp_zcoord: The z-coordinate of the mean probe position.
    """

    def __init__(self, sample_probe, mpp_xcoord, mpp_ycoord, mpp_zcoord):
        self.sample_probe = sample_probe
        self.mpp_xcoord = mpp_xcoord
        self.mpp_ycoord = mpp_ycoord
        self.mpp_zcoord = mpp_zcoord

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSMPPAtomPositionGroup(object):
    """A group of atom positions used to define the coordinate system
       of a mean probe position.
       *Not part of the FLR dictionary.*
    """
    def __init__(self):
        self.mpp_atom_position_list = []

    def add_atom_position(self, atom_position):
        self.mpp_atom_position_list.append(atom_position)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FPSMPPAtomPosition(object):
    """An atom used to describe the coordinate system for a mean probe position

       :param entity: The Entity to which the atom belongs.
       :type entity: :class:`ihm.Entity`
       :param seq_id: The sequence id of the residue.
       :param comp_id: The chemical component id of the residue.
       :param atom_id: The atom id of the atom.
       :param asym_id: The asym id of the residue.
       :param xcoord: The x-coordinate of the atom.
       :param ycoord: The y-coordinate of the atom.
       :param zcoord: The z-coordinate of the atom.
    """

    ## atoms describing the coordinate system for a mean probe position
    def __init__(self, entity, seq_id, comp_id, atom_id, asym_id,
                 xcoord, ycoord, zcoord):
        self.entity = entity
        self.seq_id = seq_id
        self.comp_id = comp_id
        self.atom_id = atom_id
        self.asym_id = asym_id
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = zcoord

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FLRData(object):
    """A collection of the fluorescence data to be added to the system.

       Instances of this class are generally added to
       :attr:`~ihm.System.flr_data`.
    """
    def __init__(self):
        self.distance_restraint_group_list = []
        self.poly_probe_conjugate_list = []
        self.fret_model_quality_list = []
        self.fret_model_distance_list = []
        self.flr_FPS_modeling_collection_list = []
        self.flr_chemical_descriptors_list = []
        ## The following dictionaries are so far only used when reading data
        self._collection_flr_experiment = {}
        self._collection_flr_exp_setting = {}
        self._collection_flr_instrument = {}
        self._collection_flr_entity_assembly = {}
        self._collection_flr_sample_condition = {}
        self._collection_flr_sample = {}
        self._collection_flr_probe_list = {}
        self._collection_flr_sample_probe_details = {}
        self._collection_flr_probe_descriptor = {}
        self._collection_flr_probe = {}
        self._collection_flr_poly_probe_position = {}
        self._collection_flr_poly_probe_position_modified = {}
        self._collection_flr_poly_probe_position_mutated = {}
        self._collection_flr_poly_probe_conjugate = {}
        self._collection_flr_fret_forster_radius = {}
        self._collection_flr_fret_calibration_parameters = {}
        self._collection_flr_fret_analysis = {}
        self._collection_flr_peak_assignment = {}
        self._collection_flr_fret_distance_restraint = {}
        self._collection_flr_fret_distance_restraint_group = {}
        self._collection_flr_fret_model_quality = {}
        self._collection_flr_fret_model_distance = {}
        self._collection_flr_fps_global_parameters = {}
        self._collection_flr_fps_modeling = {}
        self._collection_flr_fps_av_parameter = {}
        self._collection_flr_fps_av_modeling = {}
        self._collection_flr_fps_mean_probe_position = {}
        self._collection_flr_fps_mpp_atom_position = {}
        self._collection_flr_fps_mpp_modeling = {}

    def add_distance_restraint_group(self,entry):
        self.distance_restraint_group_list.append(entry)

    def add_poly_probe_conjugate(self,entry):
        self.poly_probe_conjugate_list.append(entry)

    def add_fret_model_quality(self,entry):
        self.fret_model_quality_list.append(entry)

    def add_fret_model_distance(self,entry):
        self.fret_model_distance_list.append(entry)

    def add_flr_FPS_modeling(self,entry):
        self.flr_FPS_modeling_collection_list.append(entry)

    def _occurs_in_list(self,curobject, list):
        for entry in list:
            if curobject.__dict__ == entry.__dict__:
                return True
        return False

    def _all_flr_chemical_descriptors(self):
        """Collect the chemical descriptors from the flr part.
           *The list might contain duplicates.*
        """
        self.flr_chemical_descriptors_list = []
        ## collect from all distance_restraint_groups
        for drgroup in self.distance_restraint_group_list:
            ## collect form all distance restraints
            for dr in drgroup.distance_restraint_list:
                ## collect from both sample_probe_1 and sample_probe_2
                for this_sample_probe in [dr.sample_probe_1, dr.sample_probe_2]:
                    ## collect from the probe
                    probe = this_sample_probe.probe
                    ## reactive probe
                    cur_chem_desc \
                       = probe.probe_descriptor.reactive_probe_chem_descriptor
                    self.flr_chemical_descriptors_list.append(cur_chem_desc)
                    ## chromophore
                    cur_chem_desc \
                            = probe.probe_descriptor.chromophore_chem_descriptor
                    self.flr_chemical_descriptors_list.append(cur_chem_desc)
                    ## collect from the poly_probe_position
                    this_poly_probe_position \
                            = this_sample_probe.poly_probe_position
                    ## mutated chem descriptor
                    if this_poly_probe_position.mutation_flag:
                        cur_chem_desc \
                            = this_poly_probe_position.mutated_chem_descriptor
                        self.flr_chemical_descriptors_list.append(cur_chem_desc)
                    ## modified chem descriptor
                    if this_poly_probe_position.modification_flag:
                        cur_chem_desc \
                            = this_poly_probe_position.modified_chem_descriptor
                        self.flr_chemical_descriptors_list.append(cur_chem_desc)
        ## and collect from all poly_probe_conjugates
        for this_poly_probe_conjugate in self.poly_probe_conjugate_list:
            cur_chem_desc = this_poly_probe_conjugate.chem_descriptor
            self.flr_chemical_descriptors_list.append(cur_chem_desc)
        return self.flr_chemical_descriptors_list