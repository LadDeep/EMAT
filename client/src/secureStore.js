import { setItemAsync, getItemAsync, deleteItemAsync } from "expo-secure-store";

export async function save(key, value) {
  await setItemAsync(key, value);
}

export async function getValueFor(key) {
  const result = await getItemAsync(key);
  if (result) {
    return result;
  }
}

export async function deleteKey(key) {
  await deleteItemAsync(key);
}
