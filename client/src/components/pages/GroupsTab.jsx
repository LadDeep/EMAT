import React from "react";
import { StyleSheet } from "react-native";
import { View, Button, Colors } from "react-native-ui-lib";
import { useNavigation } from "@react-navigation/native";
import { GroupList } from "../GroupList";
import data from "../../../data.json";

export const GroupsTab = () => {
  const handleNavigationToUserAccount = () => {
    //TODO: navigate to user account details page
  };
  const handleGroupRegistration = () => {
    navigation.push("GroupRegistration");
  };
  return (
    <View>
      <View>
        <View style={styles.container}>
          {data.groups ? (
            <GroupList />
          ) : (
            <Button
              label={"Add new group"}
              size={Button.sizes.medium}
              backgroundColor={Colors.blue30}
              onPress={handleGroupRegistration}
            />
          )}
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    height: "100%",
    backgroundColor: "F7F7F2",
    alignItems: "center",
    justifyContent: "center",
  },
});
