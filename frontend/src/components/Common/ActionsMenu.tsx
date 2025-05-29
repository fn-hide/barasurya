import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { FiEdit, FiTrash } from "react-icons/fi"

import type { ItemCategoryPublic, ItemPublic, UserPublic } from "../../client"
import EditUser from "../Admin/EditUser"
import EditItem from "../Items/EditItem"
import EditItemCategory from "../Items/EditItemCategory"
import EditItemUnit from "../Items/EditItemUnit"
import Delete from "./DeleteAlert"

interface ActionsMenuProps {
  type: string
  value: ItemCategoryPublic | ItemPublic | UserPublic
  disabled?: boolean
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const editUserModal = useDisclosure()
  const deleteModal = useDisclosure()
  const componentMap = {
    User: (
      <EditUser
        user={value as UserPublic}
        isOpen={editUserModal.isOpen}
        onClose={editUserModal.onClose}
      />
    ),
    Item: (
      <EditItem
        item={value as ItemPublic}
        isOpen={editUserModal.isOpen}
        onClose={editUserModal.onClose}
      />
    ),
    ItemCategory: (
      <EditItemCategory
        item={value as ItemCategoryPublic}
        isOpen={editUserModal.isOpen}
        onClose={editUserModal.onClose}
      />
    ),
    ItemUnit: (
      <EditItemUnit
        item={value as ItemUnitPublic}
        isOpen={editUserModal.isOpen}
        onClose={editUserModal.onClose}
      />
    ),
  } as const;

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          <MenuItem
            onClick={editUserModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Edit {type}
          </MenuItem>
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {componentMap[type] ?? null}
        <Delete
          type={type}
          id={value.id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  )
}

export default ActionsMenu
