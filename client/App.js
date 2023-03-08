import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SignUp from "./src/components/pages/SignUp";
import SignIn from "./src/components/pages/SignIn";
import PasswordRecovery from "./src/components/ForgotPassword";
import PasswordReset from "./src/components/RecoverPassword";
import LaunchPage from "./src/components/pages/LaunchPage";
import { useState } from "react";
const RootStack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();

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
          // TODO: Rest of the app flow
          console.log("App navigation here")
        )}
      </RootStack.Navigator>
    </NavigationContainer>
  );
}
