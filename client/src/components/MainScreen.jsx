import React, { useState } from "react";
import { View, Text, Modal, TouchableOpacity } from "react-native";
import GroupIcon from "./GroupIcon";

const MainScreen = () => {
  const [showModal, setShowModal] = useState(false);

  const handlePress = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text>Welcome to Group App!</Text>
      <GroupIcon onPress={handlePress} />
      <Modal
        visible={showModal}
        animationType="slide"
        onRequestClose={handleCloseModal}
      >
        <View
          style={{ flex: 1, alignItems: "center", justifyContent: "center" }}
        >
          <Text>Choose an option:</Text>
          <TouchableOpacity style={{ marginTop: 20 }}>
            <Text>Create a Group</Text>
          </TouchableOpacity>
          <TouchableOpacity style={{ marginTop: 20 }}>
            <Text>Join a Group</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={handleCloseModal}
            style={{ marginTop: 20 }}
          >
            <Text>Close</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
};

export default MainScreen;
