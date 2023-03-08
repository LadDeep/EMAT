import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SignUp from "./src/components/pages/SignUp";
import SignIn from "./src/components/pages/SignIn";
import PasswordRecovery from "./src/components/ForgotPassword";
import PasswordReset from "./src/components/RecoverPassword";
import LaunchPage from "./src/components/pages/LaunchPage";
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={PasswordRecovery}></Stack.Screen>
      </Stack.Navigator>
    </NavigationContainer>
  );
}
