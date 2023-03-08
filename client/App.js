import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SignUp from "./src/components/pages/register";
import SignIn from "./src/components/pages/signup";
import PasswordRecovery from "./src/components/forgotPassword";
import PasswordReset from "./src/components/recoverPassword";
import LaunchPage from "./src/components/pages/launchPage";
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
