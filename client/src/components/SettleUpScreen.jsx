import React, { useState, useEffect } from 'react'
import { DateTimePicker, Text, View} from 'react-native-ui-lib';
import { OverallGroupStandings, SettleUpExpenses } from '../api/api';
import { Button } from 'react-native-ui-lib';
import Icon from "react-native-vector-icons/MaterialIcons";
import { useNavigation } from '@react-navigation/native';
import OverallOutstandingsDisplay from './OverallOutstandingsDisplay';
import { ActivityIndicator, StyleSheet } from 'react-native';

const SettleUpScreen = ({route}) => {
  const { groupId } = route.params;
  const [userStandingDetails, setUserStandingDetails] = useState();
  const [date, setDate] = useState(new Date());
  const navigation = useNavigation();
  const [isLoading, setIsLoading] = useState(true)
;
  const handleSettleUp = ()=>{
    let transactions = userStandingDetails.map((userDetails)=>({group_id: groupId, user_id:userDetails._id, amount:userDetails.amount, last_settled_at:date }))
    console.log("transactions",transactions)
    //Call SettleUp API
    SettleUpExpenses(
      { transactions },
      (res) => {
        console.log(res);
        if (res.data.status) {
          navigation.goBack();
        } else {
          // TODO: Toast for some server error
        }
      },
      (err) => {}

      );
  }
  const handleChange = (id, value)=>{
    let userDetail = userStandingDetails.filter((user) => user._id === id);
    userDetail[0]["isChecked"] = value;
    const userDetails = userStandingDetails.map((user) =>
      user._id === id ? userDetail[0] : user
    );
    setUserStandingDetails(userDetails);
  }

  console.log("userStandingDetails: ",userStandingDetails)
  useEffect(() => {
    OverallGroupStandings(
      groupId,
      (res) => { if(res.data.status){
        const details = res.data.response.map((overallExpense) => {
            return {
              ...overallExpense,
              isChecked: true,
              isDisabled: overallExpense.total === 0,
              amount: overallExpense.total,
            }
          });
        console.log("details",details)
        setUserStandingDetails(details)
        setIsLoading(false)
      }},
      (err) => {}
    );
  }, [])
  
  console.log("userStandingDetails", userStandingDetails)
  if(isLoading){
    <View flex center>
      <ActivityIndicator size="large"/>
    </View>
  }
  return (
    <View flex marginH-48>
      <Text style={{fonWeight: "bold", fontSize: 24}}>Select members to record transcation</Text>
      <OverallOutstandingsDisplay userStandingDetails={userStandingDetails} handleCheckboxChange={handleChange}/>
      <View row center>
        <Icon style={styles.icon} name="calendar-today" size={24} />
        <DateTimePicker
          style={styles.input}
          title={"Select date"}
          mode="date"
          value={date}
          onChange={(date) => setDate(date)}
        />
      </View>
      <Button label="Settle Transactions" onPress={handleSettleUp} />
    </View>
  );
}

const styles = StyleSheet.create({
  input: {
    width: "70%",
    marginHorizontal: 8,
    marginVertical:0,
  },
  icon:{
    paddingHorizontal: 16
  }
});

export default SettleUpScreen