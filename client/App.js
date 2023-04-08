import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer, useNavigation } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SignUp from "./src/components/pages/SignUp";
import SignIn from "./src/components/pages/SignIn";
import PasswordRecovery from "./src/components/ForgotPassword";
import PasswordReset from "./src/components/RecoverPassword";
import LaunchPage from "./src/components/pages/LaunchPage";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { useState } from "react";
import { GroupsTab } from "./src/components/pages/GroupsTab";
import Activities from "./ActivitiesTab";
import JoinGroup from "./src/components/JoinGroup";
import { GroupDetailsComponent } from "./src/components/GroupDetailsComponent";
import { GroupRegistrationForm } from "./src/components/GroupRegistrationForm";
import Icon from "react-native-vector-icons/MaterialIcons";
import RegisterExpense from "./src/components/RegisterExpense";
import instance from "./src/axios";
import { deleteKey, getValueFor } from "./src/secureStore";
import AccountInfoScreen from "./src/components/pages/accountInfoScreen";
import accountDetails from "./src/components/pages/accountInfo";
import ChartDisplay from "./src/components/pages/ChartDisplay";
import ExpenseDisplay from "./src/components/ExpenseDisplay";
import UpdateExpense from "./src/components/UpdateExpense";
import GroupProvider from "./src/Context/GroupProvider";
const RootStack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();
const GroupStack = createNativeStackNavigator();
const UserDetailsStack = createNativeStackNavigator();
const BottomNavigationTab = createBottomTabNavigator();

const AuthenticationScreen = ({ route }) => {
  const { handleLogin } = route.params
  return (
    <AuthStack.Navigator>
      <AuthStack.Screen name="Launch" component={LaunchPage} />
      <AuthStack.Screen
        name="SignIn"
        component={SignIn}
        initialParams={{ handleLogin }}
      />
      <AuthStack.Screen
        name="SignUp"
        component={SignUp}
        initialParams={{ handleLogin }}
      />
      <AuthStack.Screen name="PasswordRecovery" component={PasswordRecovery} />
      <AuthStack.Screen name="PasswordReset" component={PasswordReset} />
    </AuthStack.Navigator>
  );
};
const GroupScreen = () => {
  const navigation = useNavigation();
  return (
    <GroupStack.Navigator
    >
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
      <GroupStack.Screen name="Expense" component={ExpenseDisplay} />
      <GroupStack.Screen name="Edit Expense" component={UpdateExpense} />
    </GroupStack.Navigator>
  );
};
const UserDetailsScreen = ({ route }) => {
  const { handleLogout } = route.params;
  return (
    <UserDetailsStack.Navigator
    >
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

const TabNavigation = ({ route }) => {
  const { handleLogout } = route.params

  return (
    <BottomNavigationTab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ _, color, size }) => {
          let iconName;
          if (route.name === "Groups") {
            iconName = "groups";
          } else if (route.name === "User Detail") {
            iconName = "person";
          } else if (route.name === "Activity") {
            iconName = "payments";
          } else if (route.name === "Charts") {
            iconName = "analytics";
          }
          return <Icon name={iconName} size={size} color={color} />;
        },
      })}
    >
      <BottomNavigationTab.Screen name="Groups" component={GroupScreen} />
      <BottomNavigationTab.Screen name="Activity" component={Activities} />
      <BottomNavigationTab.Screen name="Charts" component={ChartDisplay} />
      <BottomNavigationTab.Screen name="User Detail" initialParams={{ handleLogout }} component={UserDetailsScreen} />
    </BottomNavigationTab.Navigator>
  );
};

export default function App() {
  const [token, setToken] = useState(null);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(token !== null);
  const handleLogin = async () => {
    let token = await getValueFor("ACCESS_TOKEN")
    console.log("token", token, Date.now())
    setToken(token);
    instance.defaults.headers.common["Authorization"] = "Bearer " + token;
    setIsUserLoggedIn(true);
  };
  const handleLogout = async () => {
    await deleteKey("ACCESS_TOKEN")
    await deleteKey("USER_ID")
    let token = await getValueFor("ACCESS_TOKEN")

    console.log(" getValueFor", token)
    setToken(null);
    instance.defaults.headers.common["Authorization"] = null;
    setIsUserLoggedIn(false);
  };
  return (
    <NavigationContainer>
      <GroupProvider>
        <RootStack.Navigator screenOptions={{ headerShown: false }}>
          {!isUserLoggedIn ? (
            <RootStack.Screen
              name="Authentication"
              component={AuthenticationScreen}
              initialParams={{ handleLogin }}
            />
          ) : (
            <RootStack.Screen name="Root" initialParams={{ handleLogout }} component={TabNavigation} />
          )}
        </RootStack.Navigator>
      </GroupProvider>
    </NavigationContainer>
  );
}
