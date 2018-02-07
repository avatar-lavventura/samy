Install Forked Web3 Repo

```
pip install -e git+git://github.com/dangell7/web3.py.git@master#egg=web3.py
```

## Populus Test Env

```
sudo apt-get install libssl-dev
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```
### Pull Git

```
mkdir samynet
cd samynet
git init
git add .
git remote add origin https://github.com/dangell7/samy_ethereum.git
git fetch --all
git status
git checkout master
git add .
git merge origin/denis-fb-dev
virtualenv env
source env/bin/activate
pip install -U -r requirements.txt
```


### Local Samy Chain

Create Local Test Chain

```
populus chain new samynet
```

Edit Genesis

```
{
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "coinbase": "0x0000000000000000000000000000000000000000",
  "extraData": "",
  "config": {
    "chainId": 15,
    "homesteadBlock": 0
  },
  "timestamp": "0x0",
  "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "nonce": "0x0000000000000042",
  "alloc": {},
  "gasLimit": "0x2fefd8",
  "difficulty": "0x20000"
}
```

Edit Node 1 (Local) Init & Run 

```
geth --datadir /home/harpangell/PycharmProjects/samy/samy_ethereum/chains/samynet/chain_data init /home/harpangell/PycharmProjects/samy/samy_ethereum/chains/samynet/genesis.json
```

```
geth --datadir /home/harpangell/PycharmProjects/samy/samy_ethereum/chains/samynet/chain_data --verbosity 6 --ipcpath /home/harpangell/PycharmProjects/samy/samy_ethereum/chains/samynet/chain_data/geth.ipc --port 30301 --rpcport 8101 --networkid 346372 --identity "node2" --nodiscover --nat=none console 2>> samynet.log
```

Edit Node 1 (Server) Init & Run 

```
geth --datadir /home/dorian/samynet/chains/samynet/chain_data init /home/dorian/samynet/chains/samynet/genesis.json
```

```
geth --datadir /home/dorian/samynet/chains/samynet/chain_data --verbosity 6 --ipcpath /home/dorian/samynet/chains/samynet/chain_data/geth.ipc --port 30302 --rpcport 8102 --networkid 346372 --identity "node2" --nodiscover --nat=none console 2>> samynet.log
```

Init Local Test Chain

```
chains/samynet/./init_chain.sh
```

Run Local Test Chain

```
chains/samynet/./run_chain.sh
```

On Server

```
admin.nodeInfo.enode
```

On Local

```
admin.addPeer("enode://200bca6dafecec66494bb9b8296d499f07015f9b57fb8c7a2954c69f13901cd7a0a0ab653e97e182425f62af94848b7c7c68b5e3f05fa3fb928582b755053905@159.89.80.176:30302?discport=0")
admin.peers
```


iOS Address & Password

```
testing1234
0xa94a11399bdda820ea8c9cdbe22358a605a5bbf4

```