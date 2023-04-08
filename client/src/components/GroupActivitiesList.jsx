import React from "react";
import GroupActivitiesItem from "./GroupActivitiesItem";
import { GridList } from "react-native-ui-lib";

const GroupActivitiesList = ({ groupId, noOfParticipants, userId, activities }) => {
  const expenses = activities.map((expense) => {
    console.log(expense);
    const lent_or_borrowed_amount = noOfParticipants === 1 ? expense.amount: expense.amount - expense.amount / noOfParticipants;
    const user_name = expense.id===userId ? "You" : expense.user_name;
    return { ...expense, user_name, lent_or_borrowed_amount };
  });
  console.log("noOfParticipants",noOfParticipants)
  console.log("first", activities)
  return (
    //  iterate over Group data from API to display entire list
    <GridList
      horizontal={false}
      data={expenses}
      renderItem={({item} ) => (<GroupActivitiesItem groupId={groupId} activity={item} />)}
      numColumns={1}
    />
  );
};

export default GroupActivitiesList;
