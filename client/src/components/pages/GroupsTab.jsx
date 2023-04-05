import { useState, useCallback, React } from "react";
import { StyleSheet } from "react-native";
import { View, Button, Colors } from "react-native-ui-lib";
import { useNavigation, useFocusEffect } from "@react-navigation/native";
import { GroupList } from "../GroupList";
import { FAB } from "@rneui/themed";
import { FetchGroups } from "../../api/api";
export const GroupsTab = () => {
  const [groups, setGroups] = useState(null);
  const navigation = useNavigation();

  useFocusEffect(useCallback(() => {
    FetchGroups(
      (res) => {
        if(res.data.status){
          console.log(res.data.response);
        setGroups(res.data.response);
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }, []));

  const handleGroupRegistration = () => {
    navigation.push("GroupRegistration");
  };
  return (
    <>
      <View>
        <View>
          <View style={styles.container}>
            {groups && groups.length!==0 ? (
              <GroupList list={groups}/>
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
      <FAB
        icon={{ name: "group-add", color: "white" }}
        color="blue"
        placement="right"
        onPress={handleGroupRegistration}
      />
    </>
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
