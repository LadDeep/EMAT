import {React, useEffect} from "react";
import { Avatar, Text, View, Button } from "react-native-ui-lib";
import GroupActivitiesList from "./GroupActivitiesList";
import groupData from "../../api-mock-data.json";
import OverallExpenseDisplay from "./OverallExpenseDisplay";
import { StyleSheet } from "react-native";

export const GroupDetailsComponent = ({ route }) => {
  const { selectedGroup } = route.params;
  
  useEffect(() => {
    //TODO: api call for fetching overall expense list here
  }, [])
  

  return (
    <>
      <View
        style={styles.container}
      >
        <View flex row marginV-16>
          <Avatar size={76} source={{ uri: selectedGroup.imageUrl }} />
          <View paddingL-24 center>
            <Text style={styles.fontTitle}>
              {selectedGroup.name}
            </Text>
          </View>
        </View>
        <OverallExpenseDisplay />
        <View flex row center>
          <Button label={"Settle Up"} style={{ margin: 12 }}></Button>
          <Button label={"Notify"} style={{ margin: 12 }}></Button>
        </View>
      </View>
      <View flex>
        <GroupActivitiesList activities={groupData.expenses}/>
      </View>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "F7F7F2",
    marginHorizontal: 48,
  },
  detailsContainer:{ flexDirection: "row", marginVertical: 16 },
  buttonGroup:{ flexDirection: "row", justifyContent: "center" },
  fontTitle: { fontWeight: "bold", fontSize: 24 },
})