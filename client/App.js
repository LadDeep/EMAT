import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useState } from "react";
import instance from "./src/api/axios";
import { deleteKey, getValueFor } from "./src/utils/secureStore";
import GroupProvider from "./src/Context/GroupProvider";
import AuthenticationScreen from "./src/navigations/AuthenticationScreen";
import TabNavigation from "./src/navigations/TabNavigation";
const RootStack = createNativeStackNavigator();

export default function App() {
  const [token, setToken] = useState(null);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(token !== null);
  const handleLogin = async () => {
    let token = await getValueFor("ACCESS_TOKEN");
    setToken(token);
    instance.defaults.headers.common["Authorization"] = "Bearer " + token;
    setIsUserLoggedIn(true);
  };
  const handleLogout = async () => {
    await deleteKey("ACCESS_TOKEN");
    await deleteKey("USER_ID");
    let token = await getValueFor("ACCESS_TOKEN");
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
            <RootStack.Screen
              name="Root"
              initialParams={{ handleLogout }}
              component={TabNavigation}
            />
          )}
        </RootStack.Navigator>
      </GroupProvider>
    </NavigationContainer>
  );
}
