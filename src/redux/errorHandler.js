
export function formatError(response) {
  

      if (response?.data) {
        const { data, errors, title, message, error } = response
  
        if (error) {
          return Object.values(error).join(' ')
        }
    
  
        if (data) {
       return Object.values(data).join(' ')
        }
    
       
        if (errors) {
          return errors
        }
    
        return message || title
      }
    
      // return response?.error?.message ?? response?.error ?? 'Something went wrong!'
    }
    