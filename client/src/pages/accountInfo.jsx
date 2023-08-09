import { useNavigation } from "@react-navigation/native";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, Image, ActivityIndicator } from "react-native";
import { UserDetails } from "../api/api";
import { Button, View } from "react-native-ui-lib";

const accountDetails = ({ route }) => {
  const [userDetail, setUserDetail] = useState();
  const navigation = useNavigation();
  const [isLoading, setIsLoading] = useState(true);
  const { handleLogout } = route.params;

  const editAccountDetails = () => {
    navigation.push("AccountEdit");
  };
  useEffect(() => {
    UserDetails(
      (res) => {
        if (res.data.status) {
          setUserDetail(res.data.message);
          setIsLoading(false);
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }, []);
  const handleUserLogout = () => {
    handleLogout();
  };
  if (isLoading) {
    return (
      <View flex center>
        <ActivityIndicator size="large" color="blue" />
      </View>
    );
  }
  return (
    <View margin-24>
      <View style={styles.header}>
        <Image
          style={styles.avatar}
          source={require("../../assets/group/4.png")}
        />
        <View style={styles.userDetails}>
          <Text style={styles.name}>
            {userDetail?.first_name} {userDetail?.last_name}
          </Text>
          <Text style={styles.value}>{userDetail?.email}</Text>
        </View>
        <Button
          label="Edit"
          style={styles.editButton}
          onPress={editAccountDetails}
        />
      </View>
      <View center>
        <Button
          label="Logout"
          style={styles.button}
          onPress={handleUserLogout}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    padding: 20,
    paddingTop: 40,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 30,
    padding: 6,
  },

  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 20,
  },
  value: {
    flex: 1,
  },

  name: {
    fontSize: 24,
    fontWeight: "bold",
    flex: 1,
  },
  editButton: {
    backgroundColor: "darkgray",
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,

    marginLeft: 20,
  },
  editButtonText: {
    fontSize: 16,
  },
  userDetails: {
    flexDirection: "column",
  },
  details: {
    marginBottom: 30,
  },

  heading: {
    marginBottom: 15,
  },
  headingText: {
    fontWeight: "bold",
    fontSize: 25,
  },
  label: {
    fontWeight: "bold",
    width: 80,
  },
  row: {
    flexDirection: "row",
    marginBottom: 10,
    alignItems: "center",
  },
  smallLogo: {
    width: 40,
    height: 40,
    borderRadius: 40,
    marginRight: 20,
  },

  value1: {
    fontSize: 17,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
  },
});

export default accountDetails;
