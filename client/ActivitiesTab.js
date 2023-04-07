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
            let groupResponseData = response.groups;
            let settleUpResponseData = response.settleUps;
            
            
            let user_ids =  [...new Set([...groupResponseData.map(item => item.spent_by),...settleUpResponseData.map(item=>item.user_id)])];
              
            FetchOtherUserProfile({user_id: user_ids},(userResponse)=>{
              if(userResponse.data.status){
                let userResponseObject = userResponse.data.response;
                
                if(Array.isArray(userResponseObject)){
                  let userResponseIDNameMapping = {};
                  userResponseObject.forEach(item=>{
                    userResponseIDNameMapping[item.user_id] = `${item.first_name} ${item.last_name}`;
                  })
                  groupResponseData = groupResponseData.map(item=>{
                    item['created_at'] = new Date(item['created_at']['$date'])
                    item['user_name'] = userResponseIDNameMapping[item.spent_by];
                    item['activity_type'] = 'expense'
                    return item;
                  })
                  settleUpResponseData = settleUpResponseData.map(item=>{
                    item['created_at'] = new Date(item['last_settled_at']['$date'])
                    item['user_name'] = userResponseIDNameMapping[item.user_id];
                    item['activity_type'] = 'settleUp'
                    return item;
                  })
                  
                  let allResponseData = [...settleUpResponseData,...groupResponseData]
                  allResponseData.sort((a,b)=>b['created_at'] - a['created_at'])
                  allResponseData = allResponseData.map(item=>{
                    item['created_at'] = item['created_at'].toLocaleDateString('en-GB')
                    return item;
                  })
                  console.log(allResponseData)
                  setActivities(allResponseData);
                  
                }
              }
            },(userError)=>{
              console.log(userError);
            })
            
            
        }
        // setCurrencyList(res.data.message)
      },
      (err) => {
        console.log(err);
      }
    );
  },[]);

  const renderActivities = () => {
    return activities.map((activity,index) => {
      let amountStyle = styles.amountNegative;
      let formattedAmount = `- $${Math.abs(activity.amount).toFixed(2)}`;
      let formattedLabel = `You Owe`;
      if(activity.activity_type === 'expense' && ownUserID === activity.spent_by){
          amountStyle = styles.amountPositive;
          formattedAmount = `+ $${Math.abs(activity.amount).toFixed(2)}`;
          formattedLabel = 'You Get Back'
        
      }else if(activity.activity_type === 'settleUp'){
        amountStyle = styles.settleUpAmount;
        formattedAmount = `$${Math.abs(activity.amount).toFixed(2)}`
        formattedLabel = 'You Settled With'
      }
      
      

      return (
      //   <View style={styles.Maincontainer}>
      //    <Image 
      //   source={require('./assets/download.jpeg')} 
      //   style={styles.profileImage} 
      // />
        <View key={index} style={styles.activity}>
          {activity.activity_type === 'expense' ? <Text style={styles.title}>{activity.user_name} "{activity.description}".</Text>: <Text style={styles.title}>With {activity.user_name} in Group "{activity.group_name}".</Text>}
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
  settleUpAmount: {
    fontSize: 16,
    color: 'black',
  }
});

export default Activities;

