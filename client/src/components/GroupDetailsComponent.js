import { React, useState, useEffect, useLayoutEffect } from "react";
import { Avatar, Text, View, Button } from "react-native-ui-lib";
import GroupActivitiesList from "./GroupActivitiesList";
import groupData from "../../api-mock-data.json";
import OverallExpenseDisplay from "./OverallExpenseDisplay";
import { ActivityIndicator, StyleSheet } from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useNavigation } from "@react-navigation/native";
import { FAB } from "@rneui/themed";
import { getValueFor } from "../secureStore";
import {FetchOtherUserProfile } from '../api/api'
export const GroupDetailsComponent = ({ route }) => {
  const navigation = useNavigation();
  const { selectedGroup } = route.params;
  const [userIdMap, setUserIdMap] = useState();
  const [expenses, setExpenses] = useState();
  const [userId, setUserId] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const handleAddExpense = () => {
    // navigate to Add Expense page
    navigation.push("AddExpense");
  };

  const fetchUserIdFromSecureStore = async () => {
    let ownUser = await getValueFor("USER_ID");
    setUserId(ownUser);
  };
  useEffect(() => {
    //TODO: api call for fetching overall expense list here
    fetchUserIdFromSecureStore();
    FetchOtherUserProfile(
      { user_id: selectedGroup.participants },
      (res) => {
        if (res.data.status) {
          const map = new Map();
          res.data.response.forEach((element) => {
            map.set(element.user_id, element);
          });          
          setUserIdMap(map);
        }
      },
      (err) => {}
    );
  }, []);

  useEffect(() => {
    const exp = selectedGroup.expenses.map((expense) => {
      const details =
        userIdMap?.has(expense.spent_by) && userIdMap.get(expense.spent_by);
      const name =
        details?.spent_by === userId
          ? "You"
          : details?.first_name + " " + details?.last_name;
      return { ...expense, spent_by_name: name };
    });
    setExpenses(exp);
    setIsLoading(false);
  }, [userId, userIdMap]);
  useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <Icon
          name="settings"
          size={24}
          onPress={() =>
            navigation.push("GroupSettings", { selectedGroup: selectedGroup })
          }
        />
      ),
    });
  });

  if (isLoading) {
    return (
      <View flex center>
        <ActivityIndicator size="large" color="blue" />
      </View>
    );
  }
  return (
    <>
      <View style={styles.container}>
        <View flex row marginV-16>
          <Avatar size={76} source={{ uri: selectedGroup.imageUrl }} />
          <View paddingL-24 center>
            <Text style={styles.fontTitle}>{selectedGroup.group_name}</Text>
          </View>
        </View>
        <OverallExpenseDisplay />
        <View flex row center>
          <Button label={"Settle Up"} style={{ margin: 12 }}></Button>
          <Button label={"Notify"} style={{ margin: 12 }}></Button>
        </View>
      </View>
      <View flex center>
        {expenses && expenses.length !== 0 ? (
          <GroupActivitiesList activities={expenses} />
        ) : (
          <Text>No expenses</Text>
        )}
      </View>
      <FAB
        icon={{ name: "money", color: "white" }}
        color="blue"
        placement="right"
        onPress={handleAddExpense}
      />
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "F7F7F2",
    marginHorizontal: 48,
  },
  detailsContainer: { flexDirection: "row", marginVertical: 16 },
  buttonGroup: { flexDirection: "row", justifyContent: "center" },
  fontTitle: { fontWeight: "bold", fontSize: 24 },
});
