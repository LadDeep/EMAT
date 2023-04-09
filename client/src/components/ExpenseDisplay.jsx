import { useNavigation } from '@react-navigation/native'
import React from 'react'
import { Text, Button, View } from 'react-native-ui-lib'
import Icon from "react-native-vector-icons/MaterialIcons";
import {MONTHS} from '../constants/constants';
import { StyleSheet } from 'react-native';

const ExpenseDisplay = ({ route }) => {
  const navigation = useNavigation();
  const { groupId, userId, activity } = route.params;
  const handleEdit = () => {
    navigation.push("Edit Expense", { groupId, userId, activity })
  }
  const date = new Date(parseInt(activity?.created_at["$date"]));
  return (
    <View flex>
      <Text style={{ fontWeight: "bold", fontSize: 24 }}>Expense Details</Text>
      <View margin-24>
        <View row centerV>
          <Icon style={styles.icon} name="receipt" size={24} />
          <Text>{activity?.description}</Text>
        </View>
        <View row centerV>
          <Icon style={styles.icon} name="attach-money" size={24} />

          <Text>{activity?.amount}</Text>
        </View>
        <View row centerV>
          <Icon style={styles.icon} name="calendar-today" size={24} />
          <Text>
            {date.getDate() +
              " " +
              MONTHS[date.getMonth()] +
              " " +
              date.getFullYear()}
          </Text>
        </View>
        <Text>
          Added by
          {userId === activity?.spent_by ? "You" : activity?.user_name}
        </Text>
      </View>
      <Button label="Edit" onPress={handleEdit} />
    </View>
  );
}

const styles = StyleSheet.create({
  icon: {
    paddingHorizontal: 16
  }
});

export default ExpenseDisplay