import { React, useState, useEffect, useLayoutEffect, useContext } from "react";
import { Avatar, Text, View, Button, Card } from "react-native-ui-lib";
import GroupActivitiesList from "./GroupActivitiesList";
import { ActivityIndicator, StyleSheet } from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useNavigation } from "@react-navigation/native";
import { FAB } from "@rneui/themed";
import { getValueFor } from "../secureStore";
import { GroupStatsApi, UpdatedExpenseList } from '../api/api'
import GroupContext from "../Context/GroupContext";

export const GroupDetailsComponent = ({ route }) => {
  const navigation = useNavigation();
  const { selectedGroup, setExpense } = route.params;
  
  const [expenses, setExpenses] = useState();
  const [userId, setUserId] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const [mostSpender, setMostSpender] = useState()
  const [leastSpender, setLeastSpender] = useState()
  const { groupState } = useContext(GroupContext)
  console.log("THIS IS GROUPSTATE CHANGED IN GROUPDETAILCOMPONENT", groupState)
  const handleAddExpense = () => {
    // navigate to Add Expense page
    navigation.push("AddExpense", { groupId: selectedGroup.group_id, userId: userId });


  }
  const primaryColor = '#E44343';
  const secondaryColor = '#27AE60';

  const handleSettleUp = ()=>{
    navigation.push("SettleUp", {groupId: selectedGroup.group_id, userId})
  }
  const handleNotify = ()=>{
    navigation.push("Notify", {groupId: selectedGroup.group_id, userId})
  }
  const fetchUserIdFromSecureStore = async () => {
    let ownUser = await getValueFor("USER_ID");
    setUserId(ownUser);
  };

  useEffect(() => {
    //TODO: api call for fetching overall expense list here
    fetchUserIdFromSecureStore();
    GroupStatsApi(selectedGroup.group_id
      , (response) => {
        if (response.data.status) {
          console.log("Group Stats", response.data.response);
          console.log("Group Stats", response.data.response);
          console.log("Group Max", response.data.response.max.total);
          let mostSpender = response.data.response.max.first_name+" "+response.data.response.max.last_name;
          let leastSpender = response.data.response.min.first_name+" "+response.data.response.min.last_name
          setMostSpender(mostSpender)
          setLeastSpender(leastSpender)
          console.log("Group Max", response.data.response.min.total);
        }
      }, error => {
        console.log(error);
      })

    UpdatedExpenseList(selectedGroup.group_id,
      (res) => {
        console.log("This is response of updated Expenses", res.data.response)
        setExpenses(res.data.response)
      },
      (err) => { console.log("err", err) })

      setIsLoading(false)

  }, [groupState]);

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
            <Text white style={styles.boldText}>{leastSpender}</Text>
          </Card>
          <Card style={[styles.card, { backgroundColor: secondaryColor }]}>
            <Text white>Most Spending</Text>
            <Text white style={styles.boldText}>{mostSpender}</Text>
          </Card>
        </View>


        <View flex row center>
          <Button label={"Settle Up"} style={{ margin: 12 }} onPress={handleSettleUp}></Button>
          <Button label={"Notify"} style={{ margin: 12 }}  onPress={handleNotify}></Button>
        </View>
      </View>
      <View flex center>
        {expenses && expenses.length !== 0 ? (
          <GroupActivitiesList groupId={selectedGroup.group_id} noOfParticipants={selectedGroup.participants.length} userId={userId} activities={expenses} />
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
  boldText: {
    fontWeight:"bold"
  }
});
