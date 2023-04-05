import {React,useEffect,useState} from 'react';
import { StyleSheet, ScrollView, Text, View,Image } from 'react-native';
import {FetchActivitiesList, FetchOtherUserProfile} from './src/api/api';
import { getValueFor } from './src/secureStore';
// const activities = [
//   { id: 1, title: 'Dinner with friends', date: '3/10/23', amount: -40 },
//   { id: 2, title: 'Uber ride', date: '3/11/23', amount: 15 },
//   { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
//   { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
//   { id: 2, title: 'Uber ride', date: '3/11/23', amount: 15 },
//   { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
//   { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
//   { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
//   { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
//   { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
//   { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
//   { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
//   { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
// ];



const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [ownUserID,setOwnUserID] = useState(undefined);
  
  async function fetchUserIdFromSecureStore(){
    let ownUser = await getValueFor("USER_ID");
    setOwnUserID(ownUser);
  }
  useEffect(() => {
    

    fetchUserIdFromSecureStore();
    FetchActivitiesList(
      (res) => {
        if(res.data.status){
            let response = res.data.response;
            
            if(Array.isArray(response)){
              let user_ids =  [... new Set(response.map(item => item.spent_by))];
              
            FetchOtherUserProfile({user_id: user_ids},(userResponse)=>{
              if(userResponse.data.status){
                let userResponseObject = userResponse.data.response;
                
                if(Array.isArray(userResponseObject)){
                  let userResponseIDNameMapping = {};
                  userResponseObject.forEach(item=>{
                    userResponseIDNameMapping[item.user_id] = `${item.first_name} ${item.last_name}`;
                  })
                  response = response.map(item=>{
                    item['created_at'] = new Date(item['created_at']['$date']).toLocaleDateString('en-GB');
                    item['user_name'] = userResponseIDNameMapping[item.spent_by];
                    return item;
                  })
                  setActivities(response);
                }
              }
            },(userError)=>{
              console.log(userError);
            })
            }
            
        }
        // setCurrencyList(res.data.message)
      },
      (err) => {
        console.log(err);
      }
    );
  },[]);

  const renderActivities = () => {
    return activities.map((activity) => {
      let amountStyle = styles.amountNegative;
      let formattedAmount = `- $${Math.abs(activity.amount).toFixed(2)}`;
      let formattedLabel = `You Owe`;
      
      if(ownUserID === activity.spent_by){
        amountStyle = styles.amountPositive;
        formattedAmount = `+ $${Math.abs(activity.amount).toFixed(2)}`;
        formattedLabel = 'You Get Back'
      }
      

      return (
      //   <View style={styles.Maincontainer}>
      //    <Image 
      //   source={require('./assets/download.jpeg')} 
      //   style={styles.profileImage} 
      // />
        <View key={activity.expense_id} style={styles.activity}>
          <Text style={styles.title}>{activity.user_name} "{activity.description}".</Text>
          <Text style={styles.date}>{activity.created_at}</Text>
          <Text style={amountStyle}>{formattedLabel}  {formattedAmount}</Text>
        </View>
        // </View>
      );
    });
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.Activitiestitle}>Activities</Text>
      {renderActivities()}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  Maincontainer: {
    flexDirection: 'row',
    alignItems:'center'
  },
  profileImage: {
    width: 50,
    height: 50,
    borderRadius: 40,
    marginRight: 10, 
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 10,
    marginTop:32,
  },
  activity: {
    backgroundColor: '#EFF5F5',
    padding: 20,
    marginBottom: 8,
    borderRadius: 10,
  },
  title: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#000',
  },
  Activitiestitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#000',
  },
  date: {
    fontSize: 12,
    color: '#000',
    marginBottom: 8,
  },
  amountPositive: {
    fontSize: 16,
    color: 'green',
  },
  amountNegative: {
    fontSize: 16,
    color: 'red',
  },
});

export default Activities;

