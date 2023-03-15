import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SignUp from "./src/components/pages/SignUp";
import SignIn from "./src/components/pages/SignIn";
import PasswordRecovery from "./src/components/ForgotPassword";
import PasswordReset from "./src/components/RecoverPassword";
import LaunchPage from "./src/components/pages/LaunchPage";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { useState } from "react";
import { GroupsTab } from "./src/components/pages/GroupsTab";
import { ActivitiesTab } from "./ActivitiesTab";
import { FriendsTab } from "./FriendsTab";
import { ChartsTab } from "./ChartsTab";
import Icon from "react-native-vector-icons/MaterialIcons";
const RootStack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();
const BottomNavigationTab = createBottomTabNavigator();

const AuthenticationScreen = () => {
  return (
    <AuthStack.Navigator>
      <AuthStack.Screen name="Launch" component={LaunchPage} />
      <AuthStack.Screen name="SignIn" component={SignIn} />
      <AuthStack.Screen name="SignUp" component={SignUp} />
      <AuthStack.Screen name="PasswordRecovery" component={PasswordRecovery} />
      <AuthStack.Screen name="PasswordReset" component={PasswordReset} />
    </AuthStack.Navigator>
  );
};

const TabNavigation = () => {
  return (
    <BottomNavigationTab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ _, color, size }) => {
          let iconName;
          if (route.name === "Groups") {
            iconName = "groups";
          } else if (route.name === "Friends") {
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
      <BottomNavigationTab.Screen name="Groups" component={GroupsTab} />
      <BottomNavigationTab.Screen name="Friends" component={FriendsTab} />
      <BottomNavigationTab.Screen name="Activity" component={ActivitiesTab} />
      <BottomNavigationTab.Screen name="Charts" component={ChartsTab} />
    </BottomNavigationTab.Navigator>
  );
};

export default function App() {
  const [isUserLoggedIn, setisUserLoggedIn] = useState(false);
  const handleLogin = () => {
    setisUserLoggedIn(!isUserLoggedIn);
  };
  return (
    <NavigationContainer>
      <RootStack.Navigator screenOptions={{ headerShown: false }}>
        {!isUserLoggedIn ? (
          <RootStack.Screen
            name="Authentication"
            component={AuthenticationScreen}
          />
        ) : (
          <RootStack.Screen name="Root" component={TabNavigation} />
        )}
      </RootStack.Navigator>
    </NavigationContainer>
  );
}
