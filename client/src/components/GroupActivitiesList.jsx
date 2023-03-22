import React from "react";
import GroupActivitiesItem from "./GroupActivitiesItem";
import { GridList } from "react-native-ui-lib";

const GroupActivitiesList = ({ activities }) => {
  return (
    //  iterate over Group data from API to display entire list
    <GridList
      horizontal={false}
      data={activities}
      renderItem={({item} ) => (<GroupActivitiesItem activity={item} />)}
      numColumns={1}
    />
  );
};

export default GroupActivitiesList;
