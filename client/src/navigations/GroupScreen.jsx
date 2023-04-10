import { createNativeStackNavigator } from "@react-navigation/native-stack";
import ExpenseDisplay from "../components/ExpenseDisplay";
import { GroupDetailsComponent } from "../components/GroupDetailsComponent";
import { GroupRegistrationForm } from "../components/GroupRegistrationForm";
import JoinGroup from "../components/JoinGroup";
import NotifyUsersScreen from "../components/NotifyUsersScreen";
import { GroupsTab } from "../components/pages/GroupsTab";
import RegisterExpense from "../components/RegisterExpense";
import SettleUpScreen from "../components/SettleUpScreen";
import UpdateExpense from "../components/UpdateExpense";

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