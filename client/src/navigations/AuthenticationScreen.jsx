import EnterToken from "../components/pages/EnterToken";
import PasswordRecovery from "../components/pages/ForgotPassword";
import LaunchPage from "../components/pages/LaunchPage";
import SignIn from "../components/pages/SignIn";
import SignUp from "../components/pages/SignUp";
import PasswordReset from "../components/pages/RecoverPassword";
import valdateUser from "../components/pages/validateUser";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

const AuthStack = createNativeStackNavigator();

const AuthenticationScreen = ({ route }) => {
  const { handleLogin } = route.params;
  return (
    <AuthStack.Navigator>
      <AuthStack.Screen
        name="Launch"
        component={LaunchPage}
        options={{ headerShown: false }}
      />
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
      <AuthStack.Screen
        name="validateUser"
        component={valdateUser}
        initialParams={{ handleLogin }}
      />
      <AuthStack.Screen name="PasswordRecovery" component={PasswordRecovery} />
      <AuthStack.Screen name="PasswordReset" component={PasswordReset} />
      <AuthStack.Screen name="EnterToken" component={EnterToken} />
    </AuthStack.Navigator>
  );
};

export default AuthenticationScreen;
