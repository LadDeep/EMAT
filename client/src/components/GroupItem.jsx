import React from "react";
import { StyleSheet } from "react-native";
import { ListItem, Text, Avatar, View } from "react-native-ui-lib";

export const GroupItem = (props) => {
  const handleGroupItemClick = () => {
    //TODO: handle navigation to group details page
  };

  return (
    <ListItem flex style={styles.listItem} onPress={handleGroupItemClick}>
      <View flex row paddingL-24 style={{ alignItems: "center" }}>
        <Avatar
          source={{
            uri: props.item.imageUrl,
          }}
          containerStyle={{ marginRight: 12 }}
        />
        <Text style={styles.textBold}>{props.item.name}</Text>
      </View>
      {props.item.expense == 0 ? (
        <Text text24 style={styles.text}>
          You're settled
        </Text>
      ) : (
        <Text
          text24
          style={{
            paddingRight: 24,
            color: `${props.item.expense > 0 ? "red" : "green"}`,
          }}
        >
          ${props.item.expense}
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
