import json
from typing import TYPE_CHECKING, Any, List, Callable, Dict, Set
from collections import Counter

if TYPE_CHECKING:
    from Melodie import Agent


def assert_exc_occurs(exc_id: int, func: Callable):
    try:
        func()
        assert False
    except MelodieException as e:
        assert e.id == exc_id


class MelodieException(Exception):
    def __init__(self, exc_id: int, text: str):
        text = f'{text} <Error ID {exc_id}>'
        super(MelodieException, self).__init__(text)
        self.id = exc_id


class MelodieExceptions:
    class Assertions:
        @staticmethod
        def Type(name, obj, expected_type):
            if not isinstance(obj, expected_type):
                raise MelodieExceptions.General.TypeError(name, obj, expected_type)

        @staticmethod
        def IsNone(name, obj):
            if obj is not None:
                raise TypeError(f"{name} should be None, however it is not None.")

        @staticmethod
        def NotNone(name, obj):
            if obj is None:
                raise TypeError(f"{name} should not be None, however it is None.")

    class General:
        @staticmethod
        def TypeError(name, obj, expected_type: type):
            return TypeError(
                f"{name} should be a {expected_type}, however it was {type(obj)}, value {obj}")

    class Program:
        """
        Errors related to programming
        """
        ID = 1000

        class Variable:
            ID = 1010

            @staticmethod
            def VariableInvalid(var_desc: str, var_value: Any, expected_value: Any):
                return MelodieException(1011, f"Variable {var_desc} is {var_value}, but expected {expected_value} ")

            @staticmethod
            def VariableNotInSet(var_desc: str, var_value: Any, allowed_set: Set[Any]):
                return MelodieException(1012, f"Variable {var_desc} is {var_value}, not in allowed set {allowed_set} ")

        class Function:
            ID = 1020

            @staticmethod
            def FunctionArgsNumError(func: Callable, expected_arg_num: int, actual_arg_num: int):
                return MelodieException(1021,
                                        f"There should be {expected_arg_num} for function {func}, "
                                        f"but the actual argument number was {actual_arg_num}")

    class State:
        ID = 1100

        @staticmethod
        def StateNotFoundError(state, all_states):
            return MelodieException(1101,
                                    f'State {repr(state)} is not defined. All states are: {all_states}')

        @staticmethod
        def CannotMoveToNewStateError(old_state, new_state, all_possible_new_states: set):
            if len(list(all_possible_new_states)) == 0:
                return MelodieException(1102,
                                        f'Current state is {repr(old_state)}, on which the status could only move to'
                                        f' itself. However the new state was {repr(new_state)}')
            else:
                return MelodieException(1102,
                                        f'Current state is {repr(old_state)}, on which the status could only move to'
                                        f' {all_possible_new_states}. However the new state was {repr(new_state)}')

        @staticmethod
        def NotAStateAttributeError(agent_cls, state_attr: str):
            return MelodieException(1103, f'Class {agent_cls} has not defined state attribute {state_attr}')

    class Scenario:
        ID = 1200

        @staticmethod
        def ScenarioIDDuplicatedError(scenario_id):
            return MelodieException(1201, f'Scenario id {scenario_id} was duplicated, which is not allowed.')

        @staticmethod
        def ScenarioIDTypeError(scenario_id):
            return MelodieException(1202,
                                    f'Scenario id {scenario_id} should be int or str. However its type was {type(scenario_id)}.')

        @staticmethod
        def ScenarioIDNotAllNoneError(scenario_id_nones: int, scenario_nums: int):
            return MelodieException(1203,
                                    f'{scenario_id_nones} scenario(s) has/have id None, However there are totally {scenario_nums} scenarios.\n'
                                    f'If you would like to use self-increment user ids, please make sure all scenarios has id of None!')

        @staticmethod
        def NoValidScenarioGenerated(scenarios):
            return MelodieException(1204,
                                    f'The scenario manager has not generated any valid scenarios. '
                                    f'The scenarios generated by gen_scenarios() was {scenarios},'
                                    f'please make sure gen_scenarios() returns a list of Scenario.')

        @staticmethod
        def ScenariosIsEmptyList():
            return MelodieException(1205,
                                    f'The scenario manager generated an empty scenario list. '
                                    f'Please make sure gen_scenarios() returns a list of Scenario.')

        @staticmethod
        def ScenarioIDNotOfSameTypeError(id1, id2_type):
            return MelodieException(1206,
                                    f'Scenario id should be of same type, however types {type(id1)} and {id2_type}'
                                    f' detected. ')

        @staticmethod
        def ScenarioListItemTypeError(item):
            return MelodieException(1207,
                                    f'Scenario list elements are not Scenario() but a {type(item)} object with value {item}')

        @staticmethod
        def NoScenarioSheetInExcel(file_name: str):
            return MelodieException(1208, f'Melodie excel file {file_name} should have a sheet named \'scenarios\' ')

        @staticmethod
        def ParameterRedefinedError(parameter_name: str, all_params: List):
            return MelodieException(1209,
                                    f'A parameter with same name "{parameter_name}" already existed! all parameters are: {all_params}')

        # @staticmethod
        # def UnusedTableInExcel(excel_file_name: str, other_sheets: List[str]):
        #     return MelodieException(1209,
        #                             f'Melodie detected you used \'agent_params\' sheet to assign same parameter to agents in '
        #                             f'despite scenario changes. However in this case there is/are other sheet(s) {other_sheets} '
        #                             f'in the excel data {excel_file_name} which is not allowed in Melodie.')

        @staticmethod
        def ExcelAgentParamsRecordCountNotConsistentToScneario(scenario_id, scenario_agents_num: int, param_table_name,
                                                               param_num: int):
            return MelodieException(1209,
                                    f'Agent parameter sheet `{param_table_name}` contains {param_num} agents\' parameter records.\n'
                                    f'However `scenarios` sheet says there should be {scenario_agents_num}  agents '
                                    f'initially in the scenario {scenario_id}.')

        @staticmethod
        def ExcelLackAgentParamsSheet(agent_param_sheet_name, supposed_sheets=''):
            return MelodieException(1210,
                                    f"There was no excel sheet named \'agent_params\', so there is supposed to be "
                                    f"sheets named {supposed_sheets} containing agent parameters for each scenario."
                                    f" However parameter sheet `{agent_param_sheet_name}` was not found in any excel file.")

        @staticmethod
        def NoExcelFileContainsScenario(sheet_names: Dict[str, List[str]]):
            return MelodieException(1211,
                                    f'No excel file contains a sheet named \'scenarios\'. All files and their sheetnames '
                                    f'are: {json.dumps(sheet_names, indent=4)} ')

    class Agents:
        ID = 1300

        @staticmethod
        def AgentListEmpty(agent_manager):
            return MelodieException(1301, f'Agent manager {agent_manager} contains no agents!')

        @staticmethod
        def AgentPropertyNameNotExist(property_name, agent):
            return MelodieException(1302,
                                    f'Agent {agent} does not have property {property_name}. All properties are:{list(agent.__dict__.keys())}')

        @staticmethod
        def AgentIDConflict(agent_container_name: str, agent_ids: List[int]):
            c = Counter(agent_ids)
            duplicated_ids = [agent_id for agent_id, times in c.most_common() if times > 1]

            return MelodieException(1303,
                                    f'Agent container `{agent_container_name}` has duplicated agent IDs: {duplicated_ids}.')

    class Environment:
        ID = 1400

        @staticmethod
        def NoAgentListDefined(environment):
            return MelodieException(1401,
                                    f'Environment {environment} has no AgentList defined, which is not allowed!')

    class Data:
        """
        This class is used when external data is imported or exported.
        """
        ID = 1500

        @staticmethod
        def TableNameAlreadyExists(table_name: str, existed: str):
            return MelodieException(1501,
                                    f'Table Named {table_name} does not exist. All existed tables are: {existed}')

        @staticmethod
        def StaticTableNotRegistered(table_name: str, all_table_names: List[str]):
            return MelodieException(1502,
                                    f"Table '{table_name}' is not registered. All registered tables are: {all_table_names}.")

        @staticmethod
        def AttemptingReadingFromUnexistedTable(table_name):
            return MelodieException(1503, f"Table '{table_name}' does not in database.")

        @staticmethod
        def ObjectPropertyTypeUnMatchTheDataFrameError(param_name: str, param_type: type,
                                                       dataframe_dtypes: Dict[str, type], agent: 'Agent'):
            return MelodieException(1504,
                                    f"The Agent property '{param_name}' is of type {param_type}, but the corresponding column "
                                    f"of the dataframe is of type {dataframe_dtypes[param_name]}.\n"
                                    f"The agent that offended is: {agent}")

        @staticmethod
        def TableNameInvalid(table_name):
            return MelodieException(1505,
                                    f"Table name '{table_name}' is invalid."
                                    f"The expected table name should be an identifier.")

        @staticmethod
        def TableNotFound(table_name: str, all_tables: dict):
            return MelodieException(1506,
                                    f"Table '{table_name}' is not found. All registered tables are: {set(all_tables.keys())}")

        @staticmethod
        def TableColumnDoesNotMatchObjectProperty(table_name: str, column_name: str, obj: object):
            return MelodieException(1507,
                                    f"No property of object {obj.__class__.__name__} matchs column '{column_name}' "
                                    f"at table '{table_name}' ")

        @staticmethod
        def InvalidDatabaseType(database: str, supported_db_types: Set[str]):
            return MelodieException(1508,
                                    f"Melodie only support these kinds of databases: {supported_db_types}.\n"
                                    f"Database type {database} is not supported right now.\n"
                                    "Is there any spelling problems with the database name?\n"
                                    "If you do not need to write data into database, please pass `None` as DB type.")

        @staticmethod
        def NoDataframeLoaderDefined():
            return MelodieException(1509, f"No dataframe loader defined for the Simulator/Calibrator/Trainer.")

    class Tools:
        """
        This class is for errors related to dev tools such as MelodieStudio
        """
        ID = 1600

        @staticmethod
        def MelodieStudioUnAvailable():
            return MelodieException(1601,
                                    f'Connection to Melodie Studio was refused. It seems that Melodie studio is not '
                                    f'started yet. Please start Melodie Studio.')

    class Visualizer:
        """
        This class is for errors related to visualizer.
        """
        ID = 1700

        class Charts:
            ID = 1700

            @staticmethod
            def ChartNameAlreadyDefined(chart_name: str, all_chart_names: List[str]):
                return MelodieException(
                    f"Chart name '{chart_name}' is already defined. All chart names are: {all_chart_names}")
