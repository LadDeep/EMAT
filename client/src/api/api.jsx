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
const LoginUser =async(data,onSuccess,onError) =>{
  try{
    const res = await instance.post("/auth/login",data,{
      headers:{"Content-Type":"application/json"},
    });
    onSuccess && onSuccess(res);
  }catch(err){
    onError && onError(err);
  }
}

const FetchGroups = async(onSuccess, onError)=>{
  try{
    const res = await instance.get("/group/list",{
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
  } catch(err){
    onError && onError(err);
  }
}

const FetchDetailedCurrencyList = async(onSuccess, onError)=>{
  try{
    const res = await instance.get("/currency/details",{
      headers:{"Content-Type":"application/json"},
    });
    onSuccess && onSuccess(res);
  } catch(err){
    onError && onError(err);
  }
}

export { CreateUser, LoginUser, FetchGroups, FetchCurrencyList, FetchDetailedCurrencyList };