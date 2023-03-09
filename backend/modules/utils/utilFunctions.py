
def createObjectWithRequiredFields(modelInstance,required_fields,request_data,result):
    for field in required_fields:
        field_value = request_data.get(field,None)
        if field_value is not None:
            modelInstance[field] = field_value
        else:
            result["error"] = f"{field} is required"
            break
        
    if result.get("error",None) is None:
            modelInstance.save()
            result["status"] = True
            result["response"] = f"{modelInstance.__class__.__name__} saved"
    
    return result