from twocaptcha import TwoCaptcha

apiKey = "8b9085a582a46254e72ed6c3779f80db"
solver = TwoCaptcha(apiKey)

def solve(image):
  result = False
  try:
    result = solver.normal(
      image
    )
  except Exception as e:
    print("exception")
    print(e)
    
  print("balance: " + str(solver.balance()))  
  print(result)
  return result

def report(captcha_id: str, success: bool):
  solver.report(captcha_id, success)

