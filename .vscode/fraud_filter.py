print("Fraud Filter starting... ")

#  message = "This is your FINAL NOTICE. Act now to avoid losing acess!"
message = input("Enter the message you want to check: ")
input(message)
print("Message to check:", message)

# List of scammy words we want to detect
urgent_words = ["urgent", "act now", "final notice"]
print("scammy words to check:", urgent_words)

# Check if any scammy word is inside the message
found = False
for word in urgent_words:
    if word.lower() in message.lower():
        found = True

if found:
    print("⚠️ Scam detected!")
else:
    print("✅ Looks safe.")