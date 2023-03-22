import React from "react";
import { StyleSheet } from "react-native";
import { View, Avatar, Button, Colors } from "react-native-ui-lib";
import { GroupList } from "../GroupList";
import SearchComponent from "../SearchComponent";
import data from "../../../data.json";

export const GroupsTab = () => {
  const handleNavigationToUserAccount = () => {
    //TODO: navigate to user account details page
  };
  const handleGroupRegistration = () => {
    //TODO: navigate to group registration page
  };
  return (
    <View>
      <View>
        <View style={styles.headerView}>
          <Avatar
            source={{
              uri: "https://lh3.googleusercontent.com/-cw77lUnOvmI/AAAAAAAAAAI/AAAAAAAAAAA/WMNck32dKbc/s181-c/104220521160525129167.jpg",
            }}
            onPress={handleNavigationToUserAccount}
          />
          <SearchComponent />
        </View>
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
  headerView: {
    display: "flex",
    flexDirection: "row",
    alignItems: "flex-start",
    justifyContent: "space-evenly",
    paddingBottom: 8,
    paddingTop: 8,
    marginTop:45,
  },
  container: {
    backgroundColor: "F7F7F2",
    alignItems: "center",
    justifyContent: "center",
  },
});
