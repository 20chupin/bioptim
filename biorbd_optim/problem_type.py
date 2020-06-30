import numpy as np
from casadi import MX, vertcat, Function
from enum import Enum

from .dynamics import Dynamics
from .mapping import BidirectionalMapping, Mapping
from .plot import CustomPlot
from .enums import PlotType
from .path_conditions import Bounds


class Problem:
    """
    Includes methods suitable for several situations
    """

    @staticmethod
    def initialize(ocp, nlp):
        nlp["problem_type"]["type"](ocp, nlp)

    @staticmethod
    def custom(ocp, nlp):
        nlp["problem_type"]["configure"](ocp, nlp)

    @staticmethod
    def torque_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques but without muscles, must be used with dynamics without contacts.
        :param nlp: An instance of the OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_torque_driven)

    @staticmethod
    def torque_driven_with_contact(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques, without muscles, must be used with dynamics with contacts.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_torque_driven_with_contact)
        Problem.configure_contact(ocp, nlp, Dynamics.forces_from_forward_dynamics_with_contact)

    @staticmethod
    def torque_activations_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Controls u are torques and torques activations.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        nlp["nbActuators"] = nlp["nbTau"]
        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_torque_activations_driven)

    @staticmethod
    def torque_activations_driven_with_contact(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Controls u are torques and torques activations.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        nlp["nbActuators"] = nlp["nbTau"]
        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(
                ocp, nlp, Dynamics.forward_dynamics_torque_activations_driven_with_contact
            )
        Problem.configure_contact(ocp, nlp, Dynamics.forces_from_forward_dynamics_with_contact)

    @staticmethod
    def muscle_activations_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_muscles(nlp, False, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_muscle_activations_driven)

    @staticmethod
    def muscle_activations_and_torque_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        Problem.configure_muscles(nlp, False, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, nlp["problem_type"]["dynamic"])
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_torque_muscle_driven)

    @staticmethod
    def muscle_excitations_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_muscles(nlp, True, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_muscle_excitations_driven)

    @staticmethod
    def muscle_excitations_and_torque_driven(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        Problem.configure_muscles(nlp, True, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.forward_dynamics_muscle_excitations_and_torque_driven)

    @staticmethod
    def muscle_activations_and_torque_driven_with_contact(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        Problem.configure_muscles(nlp, False, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(
                ocp, nlp, Dynamics.forward_dynamics_muscle_activations_and_torque_driven_with_contact
            )
        Problem.configure_contact(
            ocp, nlp, Dynamics.forces_from_forward_dynamics_muscle_activations_and_torque_driven_with_contact
        )

    @staticmethod
    def muscle_excitations_and_torque_driven_with_contact(ocp, nlp):
        """
        Names states (nlp.x) and controls (nlp.u) and gives size to (nlp.nx) and (nlp.nu).
        Works with torques and muscles.
        :param nlp: An OptimalControlProgram class.
        """
        Problem.configure_q_qdot(nlp, True, False)
        Problem.configure_tau(nlp, False, True)
        Problem.configure_muscles(nlp, True, True)

        if "dynamic" in nlp["problem_type"]:
            Problem.configure_forward_dyn_func(ocp, nlp, Dynamics.custom)
        else:
            Problem.configure_forward_dyn_func(
                ocp, nlp, Dynamics.forward_dynamics_muscle_excitations_and_torque_driven_with_contact
            )
        Problem.configure_contact(
            ocp, nlp, Dynamics.forces_from_forward_dynamics_muscle_excitations_and_torque_driven_with_contact
        )

    @staticmethod
    def configure_q_qdot(nlp, as_states, as_controls):
        """
        Configures common settings for torque driven problems with and without contacts.
        :param nlp: An OptimalControlProgram class.
        """
        if nlp["q_mapping"] is None:
            nlp["q_mapping"] = BidirectionalMapping(
                Mapping(range(nlp["model"].nbQ())), Mapping(range(nlp["model"].nbQ()))
            )
        if nlp["q_dot_mapping"] is None:
            nlp["q_dot_mapping"] = BidirectionalMapping(
                Mapping(range(nlp["model"].nbQdot())), Mapping(range(nlp["model"].nbQdot()))
            )

        dof_names = nlp["model"].nameDof()
        q = MX()
        q_dot = MX()
        for i in nlp["q_mapping"].reduce.map_idx:
            q = vertcat(q, MX.sym("Q_" + dof_names[i].to_string(), 1, 1))
        for i in nlp["q_dot_mapping"].reduce.map_idx:
            q_dot = vertcat(q_dot, MX.sym("Qdot_" + dof_names[i].to_string(), 1, 1))

        nlp["nbQ"] = nlp["q_mapping"].reduce.len
        nlp["nbQdot"] = nlp["q_dot_mapping"].reduce.len

        legend_q = ["q_" + nlp["model"].nameDof()[idx].to_string() for idx in nlp["q_mapping"].reduce.map_idx]
        legend_qdot = ["qdot_" + nlp["model"].nameDof()[idx].to_string() for idx in nlp["q_dot_mapping"].reduce.map_idx]

        # Retrieving bounds
        q_bounds = Problem.slicing_bounds(nlp, "q")
        qdot_bounds = Problem.slicing_bounds(nlp, "q_dot")

        if as_states:
            nlp["x"] = vertcat(nlp["x"], q, q_dot)
            nlp["var_states"]["q"] = nlp["nbQ"]
            nlp["var_states"]["q_dot"] = nlp["nbQdot"]

            nlp["plot"]["q"] = CustomPlot(
                lambda x, u, p: x[: nlp["nbQ"]], plot_type=PlotType.INTEGRATED, legend=legend_q, bounds=q_bounds,
            )
            nlp["plot"]["q_dot"] = CustomPlot(
                lambda x, u, p: x[nlp["nbQ"] : nlp["nbQ"] + nlp["nbQdot"]],
                plot_type=PlotType.INTEGRATED,
                legend=legend_qdot,
                bounds=qdot_bounds,
            )
        if as_controls:
            nlp["u"] = vertcat(nlp["u"], q, q_dot)
            nlp["var_controls"]["q"] = nlp["nbQ"]
            nlp["var_controls"]["q_dot"] = nlp["nbQdot"]

            # Add plot if it happens

        nlp["nx"] = nlp["x"].rows()
        nlp["nu"] = nlp["u"].rows()

    @staticmethod
    def configure_tau(nlp, as_states, as_controls):
        """
        Configures common settings for torque driven problems with and without contacts.
        :param nlp: An OptimalControlProgram class.
        """
        if nlp["tau_mapping"] is None:
            nlp["tau_mapping"] = BidirectionalMapping(
                Mapping(range(nlp["model"].nbGeneralizedTorque())), Mapping(range(nlp["model"].nbGeneralizedTorque()))
            )

        dof_names = nlp["model"].nameDof()
        tau = MX()
        for i in nlp["tau_mapping"].reduce.map_idx:
            tau = vertcat(tau, MX.sym("Tau_" + dof_names[i].to_string(), 1, 1))

        nlp["nbTau"] = nlp["tau_mapping"].reduce.len
        legend_tau = ["tau_" + nlp["model"].nameDof()[idx].to_string() for idx in nlp["tau_mapping"].reduce.map_idx]

        if as_states:
            nlp["x"] = vertcat(nlp["x"], tau)
            nlp["var_states"]["tau"] = nlp["nbTau"]

            # Add plot if it happens, do not forget to retrieve bounds by completing the slicing bounds function
        if as_controls:
            tau_bounds = Problem.slicing_bounds(nlp, "tau")
            nlp["u"] = vertcat(nlp["u"], tau)
            nlp["var_controls"]["tau"] = nlp["nbTau"]
            nlp["plot"]["tau"] = CustomPlot(
                lambda x, u, p: u[: nlp["nbTau"]], plot_type=PlotType.STEP, legend=legend_tau, bounds=tau_bounds,
            )

        nlp["nx"] = nlp["x"].rows()
        nlp["nu"] = nlp["u"].rows()

    @staticmethod
    def configure_contact(ocp, nlp, dyn_func):
        symbolic_states = MX.sym("x", nlp["nx"], 1)
        symbolic_controls = MX.sym("u", nlp["nu"], 1)
        symbolic_param = nlp["p"]
        nlp["contact_forces_func"] = Function(
            "contact_forces_func",
            [symbolic_states, symbolic_controls, symbolic_param],
            [dyn_func(symbolic_states, symbolic_controls, symbolic_param, nlp)],
            ["x", "u", "p"],
            ["contact_forces"],
        ).expand()

        all_contact_names = []
        for elt in ocp.nlp:
            all_contact_names.extend(
                [name.to_string() for name in elt["model"].contactNames() if name.to_string() not in all_contact_names]
            )

        if "contact_forces" in nlp["plot_mappings"]:
            phase_mappings = nlp["plot_mappings"]["contact_forces"]
        else:
            contact_names_in_phase = [name.to_string() for name in nlp["model"].contactNames()]
            phase_mappings = Mapping([i for i, c in enumerate(all_contact_names) if c in contact_names_in_phase])

        nlp["plot"]["contact_forces"] = CustomPlot(
            nlp["contact_forces_func"], axes_idx=phase_mappings, legend=all_contact_names
        )

    @staticmethod
    def configure_muscles(nlp, as_states, as_controls):
        nlp["nbMuscle"] = nlp["model"].nbMuscles()
        nlp["muscleNames"] = [names.to_string() for names in nlp["model"].muscleNames()]

        combine = None
        if as_states:
            muscles = MX()
            for i in range(nlp["nbMuscle"]):
                muscles = vertcat(muscles, MX.sym(f"Muscle_{nlp['muscleNames']}_activation"))
            nlp["x"] = vertcat(nlp["x"], muscles)
            nlp["var_states"]["muscles"] = nlp["nbMuscle"]

            nx_q = nlp["nbQ"] + nlp["nbQdot"]
            nlp["plot"]["muscles_states"] = CustomPlot(
                lambda x, u, p: x[nx_q : nx_q + nlp["nbMuscle"]],
                plot_type=PlotType.INTEGRATED,
                legend=nlp["muscleNames"],
                ylim=[0, 1],
            )
            combine = "muscles_states"

        if as_controls:
            muscles = MX()
            for i in range(nlp["nbMuscle"]):
                muscles = vertcat(muscles, MX.sym(f"Muscle_{nlp['muscleNames']}_excitation"))
            nlp["u"] = vertcat(nlp["u"], muscles)
            nlp["var_controls"]["muscles"] = nlp["nbMuscle"]

            nlp["plot"]["muscles_control"] = CustomPlot(
                lambda x, u, p: u[nlp["nbTau"] : nlp["nbTau"] + nlp["nbMuscle"]],
                plot_type=PlotType.STEP,
                legend=nlp["muscleNames"],
                combine_to=combine,
                ylim=[0, 1],
            )

        nlp["nx"] = nlp["x"].rows()
        nlp["nu"] = nlp["u"].rows()

    @staticmethod
    def configure_forward_dyn_func(ocp, nlp, dyn_func):
        nlp["nu"] = nlp["u"].rows()
        nlp["nx"] = nlp["x"].rows()

        symbolic_states = MX.sym("x", nlp["nx"], 1)
        symbolic_controls = MX.sym("u", nlp["nu"], 1)
        symbolic_params = MX()
        nlp["parameters_to_optimize"] = ocp.param_to_optimize
        for key in nlp["parameters_to_optimize"]:
            symbolic_params = vertcat(symbolic_params, nlp["parameters_to_optimize"][key]["mx"])
        nlp["p"] = symbolic_params
        nlp["np"] = symbolic_params.rows()
        nlp["dynamics_func"] = Function(
            "ForwardDyn",
            [symbolic_states, symbolic_controls, symbolic_params],
            [dyn_func(symbolic_states, symbolic_controls, symbolic_params, nlp)],
            ["x", "u", "p"],
            ["xdot"],
        ).expand()

    @staticmethod
    def slicing_bounds(nlp, variable_name):
        if variable_name == 'q':
            min_bound = np.array(nlp["X_bounds"].min[:nlp["nbQ"]])
            max_bound = np.array(nlp["X_bounds"].max[:nlp["nbQ"]])
            interpolation_type = nlp["X_bounds"].min.type
        elif variable_name == 'q_dot':
            min_bound = np.array(nlp["X_bounds"].min[nlp["nbQ"]:nlp["nbQ"]+nlp["nbQdot"]])
            max_bound = np.array(nlp["X_bounds"].max[nlp["nbQ"]:nlp["nbQ"]+nlp["nbQdot"]])
            interpolation_type = nlp["X_bounds"].min.type
        elif variable_name == "muscles_states":      # TODO: Here I assume that tau is always after q and qdot in x
            min_bound = np.array(nlp["X_bounds"].min[nlp["nbQ"]+nlp["nbQdot"]:nlp["nbQ"]+nlp["nbQdot"]+nlp["nbMuscle"]])
            max_bound = np.array(nlp["X_bounds"].max[nlp["nbQ"]+nlp["nbQdot"]:nlp["nbQ"]+nlp["nbQdot"]+nlp["nbMuscle"]])
            interpolation_type = nlp["X_bounds"].min.type
        elif variable_name == "tau":  # TODO: Here I assume that tau is always in the beginning of u
            min_bound = np.array(nlp["U_bounds"].min[:nlp["nbTau"]])
            max_bound = np.array(nlp["U_bounds"].max[:nlp["nbTau"]])
            interpolation_type = nlp["U_bounds"].min.type
        elif variable_name == "muscles_control":
            min_bound = np.array(nlp["U_bounds"].min[:nlp["nbTau"]+nlp["nbMuscle"]])
            max_bound = np.array(nlp["U_bounds"].max[:nlp["nbTau"]+nlp["nbMuscle"]])
            interpolation_type = nlp["U_bounds"].min.type
        else:
            raise NotImplementedError(f"Slicing bounds for {variable_name} not implemented yet.")

        bounds = Bounds(min_bound=min_bound, max_bound=max_bound, interpolation_type=interpolation_type)
        # TODO: Change this temporary patch below by finding a solution in plot to know if nb_shoot = ns (for controls) or ns+1 (for states), cf ocp.py with X_bounds and U_bounds
        if variable_name in ['q', 'q_dot']:
            bounds.check_and_adjust_dimensions(nlp["nbQ"], nlp["ns"]+1)
        elif variable_name == 'tau':
            bounds.check_and_adjust_dimensions(nlp["nbTau"], nlp["ns"])
        return bounds

class ProblemType(Enum):
    MUSCLE_EXCITATIONS_AND_TORQUE_DRIVEN = Problem.muscle_excitations_and_torque_driven
    MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN = Problem.muscle_activations_and_torque_driven
    MUSCLE_ACTIVATIONS_DRIVEN = Problem.muscle_activations_driven
    MUSCLE_EXCITATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT = Problem.muscle_excitations_and_torque_driven_with_contact
    MUSCLE_EXCITATIONS_DRIVEN = Problem.muscle_excitations_driven
    MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT = Problem.muscle_activations_and_torque_driven_with_contact

    TORQUE_DRIVEN = Problem.torque_driven
    TORQUE_ACTIVATIONS_DRIVEN = Problem.torque_activations_driven
    TORQUE_ACTIVATIONS_DRIVEN_WITH_CONTACT = Problem.torque_activations_driven_with_contact
    TORQUE_DRIVEN_WITH_CONTACT = Problem.torque_driven_with_contact

    CUSTOM = Problem.custom
