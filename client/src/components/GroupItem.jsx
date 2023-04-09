import { useNavigation } from "@react-navigation/native";
import React from "react";
import { StyleSheet } from "react-native";
import { ListItem, Text, Avatar, View } from "react-native-ui-lib";

export const GroupItem = ({item}) => {
  const navigation = useNavigation();
  console.log(item);
  const handleGroupItemClick = () => {
    //TODO: handle navigation to group details page
    navigation.push("GroupDetails", {selectedGroup: item})
  };

  return (
    <ListItem flex style={styles.listItem} onPress={handleGroupItemClick}>
      <View flex row paddingL-24 style={{ alignItems: "center" }}>
        <Avatar
          source={""}
          containerStyle={{ marginRight: 12 }}
        />
        <Text style={styles.textBold}>{item.group_name}</Text>
      </View>
      {item.standing_amount == 0 ? (
        <Text text24 style={styles.text}>
          You're settled
        </Text>
      ) : (
        <Text
          text24
          style={{
            paddingRight: 24,
          color: `${item.standing_amount > 0 ? "green" : "red"}`,
          }}
        >
          ${parseFloat(item.standing_amount).toFixed(2)}
        </Text>
      )}
    </ListItem>
  );
};

const styles = StyleSheet.create({
  listItem: { justifyContent: "space-around", alignItems: "center" },
  textBold: { paddingLeft: 12, fontSize: 18, fontWeight: "bold" },
  text: {
    paddingRight: 24,
  },
});
