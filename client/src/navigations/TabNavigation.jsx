import Activities from "../../ActivitiesTab";
import ChartDisplay from "../components/pages/ChartDisplay";
import GroupScreen from "./GroupScreen";
import UserDetailsScreen from "./UserDetailsScreen";
import Icon from "react-native-vector-icons/MaterialIcons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

const BottomNavigationTab = createBottomTabNavigator();

const getIcons = ({ color, size, route }) => {
  if (route.name === "Groups") {
    return <Icon name={"groups"} size={size} color={color} />;
  } else if (route.name === "User Detail") {
    return <Icon name={"person"} size={size} color={color} />;
  } else if (route.name === "Activity") {
    return <Icon name={"payments"} size={size} color={color} />;
  } else if (route.name === "Charts") {
    return <Icon name={"analytics"} size={size} color={color} />;
  }
};

const TabNavigation = ({ route }) => {
  const { handleLogout } = route.params;

  return (
    <BottomNavigationTab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({color, size})=>getIcons({ color, size, route }),
      })}
    >
      <BottomNavigationTab.Screen name="Groups" component={GroupScreen} />
      <BottomNavigationTab.Screen name="Activity" component={Activities} />
      <BottomNavigationTab.Screen name="Charts" component={ChartDisplay} />
      <BottomNavigationTab.Screen
        name="User Detail"
        initialParams={{ handleLogout }}
        component={UserDetailsScreen}
      />
    </BottomNavigationTab.Navigator>
  );
};

export default TabNavigation;
