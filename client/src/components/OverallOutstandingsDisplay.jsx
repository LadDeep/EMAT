import React from "react";
import { View, GridList, ListItem, Checkbox, Text } from "react-native-ui-lib";

const OverallOutstandingsDisplay = ({
  userStandingDetails,
  handleCheckboxChange,
}) => {
  console.log("disp", userStandingDetails);
  return (
    <>
      {userStandingDetails && (
        <View>
          <GridList
            horizontal={false}
            data={userStandingDetails}
            renderItem={({ item }) => (
              <ListItem style={{ width: "80%" }}>
                <View
                  flex
                  row
                  marginH-16
                  style={{ justifyContent: "space-between" }}
                >
                <Checkbox
                  value={item.isChecked}
                  label={item.user_name}
                  isDisabled={item.isDisabled}
                  onValueChange={(value) =>
                    handleCheckboxChange(item._id, value)
                  }
                />
                <View row centerV>
                  {item.amount >= 0 ? (
                    item.amount === 0 ? (
                      <Text>You're settled</Text>
                      ) : (
                        <>
                        <Text>Get Back </Text>
                        <Text style={{ color: "green" }}>
                          ${parseFloat(item.amount).toFixed(2)}
                        </Text>
                      </>
                    )
                    ) : (
                    <>
                      <Text>Pay Back </Text>
                      <Text style={{ color: "red" }}>
                        ${parseFloat(item.amount).toFixed(2)}
                      </Text>
                    </>
                  )}
                  </View>
                </View>
              </ListItem>
            )}
            keyExtractor={(item) => item._id}
            numColumns={1}
          />
        </View>
      )}
    </>
  );
};

export default OverallOutstandingsDisplay;
