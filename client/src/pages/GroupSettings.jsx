import React from "react";
import { View, Avatar, Text, TouchableOpacity } from "react-native-ui-lib";
import Icon from "react-native-vector-icons/MaterialIcons";
import { StyleSheet } from "react-native";
import MemberList from "../MemberList";
import { useNavigation } from "@react-navigation/native";

const GroupSettings = ({route}) => {
  const { selectedGroup } = route.params;
  const navigation = useNavigation();
  return (
    <View >
      <View row center marginV-16>
        <Avatar size={56} source={{ uri: selectedGroup.imageUrl }} />
        <View paddingL-24>
          <Text style={styles.fontTitle}>{selectedGroup.name}</Text>
          <Text>Created by someone on somedate</Text>
        </View>
        <Icon
          name="edit"
          size={24}
          color="blue"
          onPress={() => navigation.push("GroupDetailsEdit", {id: selectedGroup.group_id, name: selectedGroup.group_name, currency: selectedGroup.group_currency})}
          style={{ marginLeft: 16 }}
        />
      </View>
      <Text marginH-18 style={styles.titleMedium}>Members</Text>
      <MemberList members={[]} />
      <View marginH-18>
        <TouchableOpacity>
          <View row centerV marginV-16>
            <Icon
              name="person-add"
              size={28}
              color="blue"
              onPress={() => console.log("Add person")}
            />
            <Text marginH-16 style={styles.titleMedium}>
              Add members
            </Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity>
          <View row centerV marginV-16>
            <Icon
              name="share"
              size={28}
              color="blue"
              onPress={() => console.log("Show group code")}
            />
            <Text marginH-16 style={styles.titleMedium}>
              Share group code
            </Text>
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  fontTitle: { fontWeight: "bold", fontSize: 24 },
  titleSmall: { fontWeight: "bold", fontSize: 16 },
  titleMedium: { fontWeight: "600", fontSize: 18 },
});

export default GroupSettings;
