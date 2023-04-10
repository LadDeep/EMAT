import accountDetails from "../pages/accountInfo";
import AccountInfoScreen from "../pages/accountInfoScreen";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

const UserDetailsStack = createNativeStackNavigator();

const UserDetailsScreen = ({ route }) => {
  const { handleLogout } = route.params;
  return (
    <UserDetailsStack.Navigator>
      <UserDetailsStack.Screen
        name="AccountDetails"
        component={accountDetails}
        initialParams={{ handleLogout }}
      />
      <UserDetailsStack.Screen
        name="AccountEdit"
        component={AccountInfoScreen}
      />
    </UserDetailsStack.Navigator>
  );
};

export default UserDetailsScreen;
