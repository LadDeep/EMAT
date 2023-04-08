import { useState, useCallback, React } from "react";
import { StyleSheet,Text, Modal, TouchableOpacity } from "react-native";
import { View, Button, Colors, } from "react-native-ui-lib";
import { useNavigation, useFocusEffect } from "@react-navigation/native";
import { GroupList } from "../GroupList";
import GroupIcon from '../GroupIcon';

import { FetchGroups } from "../../api/api";
export const GroupsTab = () => {
  const [groups, setGroups] = useState(null);
  const navigation = useNavigation();
  const [showModal, setShowModal] = useState(false);

  const handlePress = () => {
      setShowModal(true);
  };

  const handleCloseModal = () => {
      setShowModal(false);
  };

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
    handleCloseModal();
    navigation.push("GroupRegistration");
  };

  const handleJoinGroup = () => {
    handleCloseModal();
    navigation.push("JoinGroup");
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
      <GroupIcon onPress={handlePress} />
      <Modal visible={showModal} animationType="slide" onRequestClose={handleCloseModal}>
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
              <Text>Choose an option:</Text>
              <TouchableOpacity style={{ marginTop: 20 }} onPress={handleGroupRegistration}>
                  <Text>Create a Group</Text>
              </TouchableOpacity>
              <TouchableOpacity style={{ marginTop: 20 }} onPress={handleJoinGroup}>
                  <Text>Join a Group</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleCloseModal} style={{ marginTop: 20 }}>
                  <Text>Close</Text>
              </TouchableOpacity>
          </View>
      </Modal>
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
