import React from 'react';
import { StyleSheet, ScrollView, Text, View,Image } from 'react-native';

const activities = [
  { id: 1, title: 'Dinner with friends', date: '3/10/23', amount: -40 },
  { id: 2, title: 'Uber ride', date: '3/11/23', amount: 15 },
  { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
  { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
  { id: 2, title: 'Uber ride', date: '3/11/23', amount: 15 },
  { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
  { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
  { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
  { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
  { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
  { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
  { id: 3, title: 'Movie tickets', date: '3/12/23', amount: -25 },
  { id: 4, title: 'Grocery shopping', date: '3/14/23', amount: 80 },
];

const Activities = () => {
  const renderActivities = () => {
    return activities.map((activity) => {
      const amountStyle = activity.amount < 0 ? styles.amountNegative : styles.amountPositive;
      const formattedAmount = `${activity.amount > 0 ? '+' : '-'}$${Math.abs(activity.amount)}`;
      const formattedLabel = `${activity.amount > 0 ? 'You Get Back' : 'You Owe'}`;
      return (
      //   <View style={styles.Maincontainer}>
      //    <Image 
      //   source={require('./assets/download.jpeg')} 
      //   style={styles.profileImage} 
      // />
        <View key={activity.id} style={styles.activity}>
          <Text style={styles.title}>#name_of_user added "{activity.title}".</Text>
          <Text style={styles.date}>{activity.date}</Text>
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

