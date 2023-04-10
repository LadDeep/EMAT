import EnterToken from "../pages/EnterToken";
import PasswordRecovery from "../pages/ForgotPassword";
import LaunchPage from "../pages/LaunchPage";
import SignIn from "../pages/SignIn";
import SignUp from "../pages/SignUp";
import PasswordReset from "../pages/RecoverPassword";
import valdateUser from "../pages/validateUser";
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
