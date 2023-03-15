import React from "react";
import { GridList } from "react-native-ui-lib";
import data from "../../data.json"
import { GroupItem } from "./GroupItem";

export const GroupList = () => {
  return (
    <GridList
      horizontal={false}
      data={data.groups}
      renderItem={({ item }) => (
        <GroupItem item={item}/>
      )}
      numColumns={1}
    />
  );
};
