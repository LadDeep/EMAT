import { createNativeStackNavigator } from "@react-navigation/native-stack";
import ExpenseDisplay from "../pages/ExpenseDisplay";
import { GroupDetailsComponent } from "../components/GroupDetailsComponent";
import { GroupRegistrationForm } from "../pages/GroupRegistrationForm";
import JoinGroup from "../pages/JoinGroup";
import NotifyUsersScreen from "../pages/NotifyUsersScreen";
import { GroupsTab } from "../pages/GroupsTab";
import RegisterExpense from "../pages/RegisterExpense";
import SettleUpScreen from "../pages/SettleUpScreen";
import UpdateExpense from "../pages/UpdateExpense";

const GroupStack = createNativeStackNavigator();
const GroupScreen = () => {
    return (
      <GroupStack.Navigator>
        <GroupStack.Screen
          name="GroupsTab"
          component={GroupsTab}
          options={{ headerSearchBarOptions: true }}
        />
        <GroupStack.Screen
          name="GroupRegistration"
          component={GroupRegistrationForm}
        />
        <GroupStack.Screen
          name="JoinGroup"
          component={JoinGroup}
        />
  
        <GroupStack.Screen
          name="GroupDetails"
          component={GroupDetailsComponent}
        />
        <GroupStack.Screen name="AddExpense" component={RegisterExpense} />
        <GroupStack.Screen name="SettleUp" component={SettleUpScreen} />
        <GroupStack.Screen name="Expense" component={ExpenseDisplay} />
        <GroupStack.Screen name="Edit Expense" component={UpdateExpense} />
        <GroupStack.Screen name="Notify" component={NotifyUsersScreen} />
      </GroupStack.Navigator>
    );
  };
  
  export default GroupScreen;