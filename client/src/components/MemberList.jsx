import { useState, useEffect, React } from "react";
import { StyleSheet } from "react-native";
import { GridList, ListItem, Text, View } from "react-native-ui-lib";

const MemberList = (props) => {
  const [members, setMembers] = useState([
    { full_name: "Alpha", email: "alpha@test.com" },
    { full_name: "Nuemro", email: "neumro@test.com" },
  ]);
  useEffect(() => {
    // fetch members from id list
  }, []);

  return (
    //  iterate over Group data from API to display entire list
    <GridList
      horizontal={false}
      data={members}
      style={{marginHorizontal:32}}
      renderItem={({ item }) => (
        <ListItem>
          <View row center>
            <View >
              <Text style={styles.titleSmall}>{item.full_name}</Text>
              <Text>{item.email}</Text>
            </View>
          </View>
        </ListItem>
      )}
      numColumns={1}
    />
  );
};

const styles = StyleSheet.create({
  titleSmall: { fontWeight: "bold", fontSize: 16 },
});

export default MemberList;
