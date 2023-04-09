import { useState, useCallback, React, useContext, useEffect } from "react";
import { ActivityIndicator, StyleSheet } from "react-native";
import { View, Button, Colors, Modal, Text, TouchableOpacity } from "react-native-ui-lib";
import { useNavigation, useFocusEffect } from "@react-navigation/native";
import { GroupList } from "../GroupList";
import { FetchGroups } from "../../api/api";
import { FAB } from "@rneui/base";
import GroupContext from "../../Context/GroupContext";

export const GroupsTab = () => {
  const [groups, setGroups] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const { groupState } = useContext(GroupContext);
  const navigation = useNavigation();
  const [isLoading, setIsLoading] = useState(true);
  console.log("Group State in GroupTab Value", groupState)

  const handlePress = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };


  console.log("showModal", showModal)
  useFocusEffect(useCallback(() => {
    FetchGroups(
      (res) => {
        if (res.data.status) {
          console.log("------------------------------------------", res.data.response);
          setGroups(res.data.response);
          setIsLoading(false);
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }, []));
  useEffect(() => {
    FetchGroups(
      (res) => {
        if (res.data.status) {
          console.log("++++++++++++++++++++++++++++++++++++++++", res.data.response);
          setGroups(res.data.response);
          setIsLoading(false);
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }, [groupState])

  const handleGroupRegistration = () => {
    handleCloseModal();
    navigation.push("GroupRegistration");
    setShowModal(false);
  };

  const handleJoinGroup = () => {
    handleCloseModal();
    navigation.push("JoinGroup");
    setShowModal(false);
  };

  if(isLoading){
    return (
      <View flex center>
        <ActivityIndicator size="large" color="blue" />
      </View>
    );
  }

  return (
    <>
      <View>
        <View>
          <View style={styles.container}>
            {groups && groups.length !== 0 ? (
              <GroupList list={groups} />
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
        onPress={handlePress}
      />
      <Modal
        visible={showModal}
        animationType="slide"
        onRequestClose={handleCloseModal}
      >
        <View
          style={{ flex: 1, alignItems: "center", justifyContent: "center" }}
        >
          <Text style={styles.fontTitle}>Choose an option:</Text>
          <View center>
            <TouchableOpacity
              onPress={handleGroupRegistration}
              style={{ marginTop: 20 }}
            >
              <Text style={styles.option}>Create a Group</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleJoinGroup}>
              <Text style={styles.option}>Join a Group</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleCloseModal} style={styles.close}>
              <Text>Close</Text>
            </TouchableOpacity>
          </View>
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
  option: {
    backgroundColor: "blue",
    color: "white",
    paddingHorizontal: 24,
    paddingVertical: 12,
    marginVertical: 12,
    borderRadius: 25,
    width: "50%",
  },
  close: {
    backgroundColor: "lightgray",
    color: "white",
    paddingHorizontal: 24,
    paddingVertical: 12,
    marginVertical: 12,
    borderRadius: 25,
    width: "50%",
  },
  fontTitle: { fontWeight: "bold", fontSize: 24, marginVertical: 12 },
});
