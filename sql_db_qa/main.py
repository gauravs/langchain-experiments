import sys

from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

db = SQLDatabase.from_uri("sqlite:///db/Chinook.db")
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def main():
  args_string = ' '.join(sys.argv[1:])
  db_chain.run(args_string)

if __name__ == "__main__":
  main()
