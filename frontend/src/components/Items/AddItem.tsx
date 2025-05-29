import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Select,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import { type ApiError, type ItemCreate, ItemsService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddItemProps {
  isOpen: boolean
  onClose: () => void
}

const AddItem = ({ isOpen, onClose }: AddItemProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ItemCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      title: "",
      description: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: ItemCreate) =>
      ItemsService.createItem({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Item created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] })
    },
  })

  const onSubmit: SubmitHandler<ItemCreate> = (data) => {
    mutation.mutate(data)
  }

  const frameworks = [
    {
      id: "uuid1",
      label: "Basic Plan",
      value: "basic",
      description: "$9/month - Perfect for small projects",
    },
    {
      id: "uuid2",
      label: "Pro Plan",
      value: "pro",
      description: "$29/month - Advanced features",
    },
    {
      id: "uuid3",
      label: "Business Plan",
      value: "business",
      description: "$99/month - Enterprise-grade solutions",
    },
    {
      id: "uuid4",
      label: "Enterprise Plan",
      value: "enterprise",
      description: "Custom pricing - Tailored solutions",
    },
  ]

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Add Item</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.title}>
              <FormLabel htmlFor="title">Title</FormLabel>
              <Input
                id="title"
                {...register("title", {
                  required: "Title is required.",
                })}
                placeholder="Title"
                type="text"
              />
              {errors.title && (
                <FormErrorMessage>{errors.title.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.item_category_id} mt={4}>
              <FormLabel htmlFor="item_category_id">Category</FormLabel>
              <Select
                id="item_category_id"
                {...register("item_category_id", {
                  required: "Category of item is required."
                })}
                placeholder="Select the category of item">
                {frameworks.map((plan) => (
                  <option key={plan.value} value={plan.value}>
                    {plan.label}
                  </option>
                ))}
              </Select>
              {errors.item_category_id && (
                <FormErrorMessage>{errors.item_category_id.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.item_unit_id} mt={4}>
              <FormLabel htmlFor="item_unit_id">Unit</FormLabel>
              <Select
                id="item_unit_id"
                {...register("item_unit_id", {
                  required: "Unit of item is required."
                })}
                placeholder="Select the unit of item">
                {frameworks.map((plan) => (
                  <option key={plan.value} value={plan.value}>
                    {plan.label}
                  </option>
                ))}
              </Select>
              {errors.item_unit_id && (
                <FormErrorMessage>{errors.item_unit_id.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="description">Description</FormLabel>
              <Input
                id="description"
                {...register("description")}
                placeholder="Description"
                type="text"
              />
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default AddItem
