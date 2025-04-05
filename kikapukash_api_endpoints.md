
# KikapuKash API Endpoints

## 👤 Authentication & Users
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/auth/register/` | `POST` | Register a new user |
| `/api/auth/login/` | `POST` | JWT login |
| `/api/auth/profile/` | `GET/PUT` | View/update current user |
| `/api/users/` | `GET` | Admin: List all users |
| `/api/users/<id>/` | `GET` | Admin: Get user details |

---

## 👥 Savings Groups
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/groups/` | `GET, POST` | List all groups / create new group |
| `/api/groups/<id>/` | `GET, PUT, DELETE` | Group details, update, or delete |
| `/api/groups/<id>/join/` | `POST` | Request to join group |
| `/api/groups/<id>/members/` | `GET` | List members of the group |
| `/api/groups/<id>/approve-member/<user_id>/` | `POST` | Admin approves member |
| `/api/groups/<id>/withdrawal-rules/` | `GET, PUT` | View/update rules (admin only) |

---

## 💰 Wallets & Transactions
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/wallets/` | `GET` | List wallets for current user |
| `/api/wallets/<id>/` | `GET` | View wallet details |
| `/api/transactions/` | `GET, POST` | List or create transactions (contributions, transfers, etc) |
| `/api/transactions/<id>/` | `GET` | Transaction details |

---

## 🧾 Contributions & Balances
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/groups/<id>/contribute/` | `POST` | Contribute to group |
| `/api/groups/<id>/balances/` | `GET` | Get all members' balances (admin only) |
| `/api/groups/<id>/balance/` | `GET` | Get current user's balance in group |

---

## 🏦 Withdrawals
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/withdrawals/` | `POST` | Submit withdrawal request |
| `/api/withdrawals/<id>/` | `GET` | View specific withdrawal |
| `/api/withdrawals/group/<group_id>/` | `GET` | Group admin: view pending/approved requests |
| `/api/withdrawals/<id>/approve/` | `POST` | Admin approves request |
| `/api/withdrawals/<id>/reject/` | `POST` | Admin rejects request |

---

## 📊 Dashboard / Stats 
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/dashboard/overview/` | `GET` | See user contributions, group participation, total saved |
| `/api/admin/stats/` | `GET` | Admin view of all group activity |
