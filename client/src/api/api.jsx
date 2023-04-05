import instance from '../axios'

const CreateUser = async (data, onSuccess, onError) => {
  try {

    const res = await instance.post("/auth/register", data, {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
};
const LoginUser = async (data, onSuccess, onError) => {
  try {
    const res = await instance.post("/auth/login", data, {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}
const UpdateUser = async (data, onSuccess, onError) => {
  try {
    const res = await instance.put("/profie/update", data, {
      headers: {
        "Content-Type": "application/json"
      },
    })
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}

const FetchGroups = async (onSuccess, onError) => {
  try {
    const res = await instance.get("/group/list", {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}

const RegisterGroup = async(data, onSuccess, onError)=>{
  try{
    const res = await instance.post("/group/register", data,{
      headers:{"Content-Type":"application/json"},
    });
    onSuccess && onSuccess(res);
  } catch(err){
    onError && onError(err);
  }
}

const FetchCurrencyList = async(onSuccess, onError)=>{
  try{
    const res = await instance.get("/currency/list",{
      headers:{"Content-Type":"application/json"},
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}

const FetchDetailedCurrencyList = async (onSuccess, onError) => {
  try {
    const res = await instance.get("/currency/details", {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}
const UserDetails = async (onSuccess, onError) => {
  try {
    const res = await instance.get("/profile/user", {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}

const FetchActivitiesList = async (onSuccess, onError) => {
  try {
    const res = await instance.get("/activities/list", {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}
const FetchOtherUserProfile = async (data, onSuccess, onError) => {
  try {
    const res = await instance.post("/profile/other_user_details", data, {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
}

const FetchProfileEmail = async (data, onSuccess, onError) => {
  try {
    const res = await instance.get("/profile/email", {
      headers: { "Content-Type": "application/json" },
    });
    onSuccess && onSuccess(res);
  } catch (err) {
    onError && onError(err);
  }
};
export {
  CreateUser,
  LoginUser,
  FetchGroups,
  RegisterGroup,
  FetchCurrencyList,
  FetchDetailedCurrencyList,
  UpdateUser,
  FetchActivitiesList,
  FetchOtherUserProfile,
  UserDetails,
  FetchProfileEmail,
};
