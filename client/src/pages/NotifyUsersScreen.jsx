import React, { useState, useEffect } from "react";
import { DateTimePicker, Text, View, Button } from "react-native-ui-lib";
import { NotifyUsers, OverallGroupStandings } from "../api/api";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useNavigation } from "@react-navigation/native";
import OverallOutstandingsDisplay from "../components/OverallOutstandingsDisplay";
import { ActivityIndicator, StyleSheet } from "react-native";

const NotifyUsersScreen = ({ route }) => {
  const { groupId } = route.params;
  const [userStandingDetails, setUserStandingDetails] = useState();
  const [date, setDate] = useState(new Date());
  const navigation = useNavigation();
  const [isLoading, setIsLoading] = useState(true);
  const handleNotify = () => {
    // Notify users
    let userDetails = userStandingDetails.filter((user) => user.isChecked);
    let userList = userDetails.map((user) => ({
      user_id: user._id,
      amount: Math.abs(user.amount),
    }));

    NotifyUsers(
      { group_id: groupId, notify_users: userList },
      (res) => {
        console.log(res);
        if (res.data.status) {
          navigation.goBack();
        }
      },
      (err) => {}
    );
  };
  const handleChange = (id, value) => {
    let userDetail = userStandingDetails.filter((user) => user._id === id);
    userDetail[0]["isChecked"] = value;
    const userDetails = userStandingDetails.map((user) =>
      user._id === id ? userDetail[0] : user
    );
    setUserStandingDetails(userDetails);
  };

  useEffect(() => {
    OverallGroupStandings(
      groupId,
      (res) => {
        if (res.data.status) {
          const details = res.data.response.map((overallExpense) => {
            return {
              ...overallExpense,
              isChecked: true,
              isDisabled: overallExpense.total === 0,
              amount: overallExpense.total,
            };
          });
          setUserStandingDetails(details);
          setIsLoading(false);
        }
      },
      (err) => {}
    );
  }, []);

  if (isLoading) {
    return (
      <View flex center>
        <ActivityIndicator size="large" color="blue" />
      </View>
    );
  }
  return (
    <View flex marginH-48>
      <Text style={{ fonWeight: "bold", fontSize: 24 }}>
        Select members to notify
      </Text>
      <OverallOutstandingsDisplay
        userStandingDetails={userStandingDetails}
        handleCheckboxChange={handleChange}
      />
      <View row centerV>
        <Icon style={styles.icon} name="calendar-today" size={24} />
        <DateTimePicker
          style={styles.input}
          title={"Select date"}
          mode="date"
          value={date}
          onChange={(date) => setDate(date)}
        />
      </View>
      <View center>
        <Button label="Notify" style={styles.button} onPress={handleNotify} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    width: "70%",
    marginHorizontal: 8,
    marginVertical: 0,
  },
  icon: {
    paddingHorizontal: 16,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
  },
});

export default NotifyUsersScreen;
