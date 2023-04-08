import { React, useState, useEffect, useLayoutEffect } from "react";
import { Avatar, Text, View, Button, Card } from "react-native-ui-lib";
import GroupActivitiesList from "./GroupActivitiesList";
import { ActivityIndicator, StyleSheet } from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useNavigation } from "@react-navigation/native";
import { FAB } from "@rneui/themed";
import { getValueFor } from "../secureStore";
import { FetchGroups, FetchOtherUserProfile, GroupStatsApi } from '../api/api'

export const GroupDetailsComponent = ({ route }) => {
  const navigation = useNavigation();
  const { selectedGroup, setExpense } = route.params;
  const [userIdMap, setUserIdMap] = useState();
  const [expenses, setExpenses] = useState();
  const [userId, setUserId] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const [Spending, setSpending] = useState()
  const [lending, setLending] = useState()
  const handleAddExpense = () => {
    // navigate to Add Expense page
    navigation.push("AddExpense", { groupId: selectedGroup.group_id, userId: userId });
    console.log("This is Selected Group", selectedGroup)
    if (setExpense !== undefined) {
      setExpenses(setExpense)
    }

  }
  const primaryColor = '#E44343';
  const secondaryColor = '#27AE60';
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
      (err) => { console.log(err) }
    );

    GroupStatsApi(selectedGroup.group_id
      , (response) => {
        if (response.data.status) {
          console.log("Group Stats", response.data.response);
          console.log("Group Max", response.data.response.max.total);
          setSpending(response.data.response.max.total)
          setLending(response.data.response.min.total)
          console.log("Group Max", response.data.response.min.total);
        }
      }, error => {
        console.log(error);
      })
  }, [navigation.isFocused]);
  useEffect(() => {
    const exp = selectedGroup.expenses.map((expense) => {
      const details =
        userIdMap?.has(expense.spent_by) && userIdMap.get(expense.spent_by);
      const name =
        expense.spent_by === userId
          ? "You"
          : details?.first_name + " " + details?.last_name;
      const lent_or_borrowed_amount = expense.amount - expense.amount / selectedGroup.participants.length;
      return { ...expense, spent_by_name: name, lent_or_borrowed_amount };
    });
    setExpenses(exp);
    setIsLoading(false);
  }, [userId, userIdMap, navigation.isFocused]);
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

        <View flex row centerV spread>
          <Text style={styles.fontTitle}>{selectedGroup.group_name}</Text>
          <Avatar size={76} source={{ uri: selectedGroup.imageUrl }} />
        </View>

        <View style={styles.cardContainer}>
          <Card style={[styles.card, { backgroundColor: primaryColor }]}>
            <Text white>Least Spending</Text>
            <Text white>{lending}</Text>
          </Card>
          <Card style={[styles.card, { backgroundColor: secondaryColor }]}>
            <Text white>Most Spending</Text>
            <Text white>{Spending}</Text>
          </Card>
        </View>


        <View flex row center>
          <Button label={"Settle Up"} style={{ margin: 12 }}></Button>
          <Button label={"Notify"} style={{ margin: 12 }}></Button>
        </View>
      </View>
      <View flex center>
        {expenses && expenses.length !== 0 ? (
          <GroupActivitiesList groupId={selectedGroup.group_id} activities={expenses} />
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
    marginHorizontal: 24,
  },
  detailsContainer: { flexDirection: "row", marginVertical: 16 },
  buttonGroup: { flexDirection: "row", justifyContent: "center" },
  fontTitle: { fontWeight: "bold", fontSize: 24 },
  cardContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    // paddingHorizontal: 20,
    // paddingTop: 20,
  },
  card: {
    width: '47%',
    height: 80,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
