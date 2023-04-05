import React from "react";
import { GridList } from "react-native-ui-lib";
import { GroupItem } from "./GroupItem";

export const GroupList = ({list}) => {
  return (
    <GridList
      horizontal={false}
      data={list}
      renderItem={({ item }) => (
        <GroupItem item={item}/>
      )}
      numColumns={1}
    />
  );
};
