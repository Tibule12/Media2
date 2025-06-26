import { mount } from '@vue/test-utils'
import Register from '../Register.vue'
import axios from 'axios'

jest.mock('axios')

describe('Register.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Register, {
      data() {
        return {
          username: '',
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          fullName: '',
          profilePicture: null,
          error: null,
        }
      }
    })
  })

  it('renders registration form inputs', () => {
    expect(wrapper.find('input[placeholder="Username"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Email"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Password"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="First Name"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Last Name"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Full Name"]').exists()).toBe(true)
    expect(wrapper.find('input[type="file"]').exists()).toBe(true)
  })

  it('updates data properties on input', async () => {
    const usernameInput = wrapper.find('input[placeholder="Username"]')
    await usernameInput.setValue('testuser')
    expect(wrapper.vm.username).toBe('testuser')

    const fullNameInput = wrapper.find('input[placeholder="Full Name"]')
    await fullNameInput.setValue('Test User')
    expect(wrapper.vm.fullName).toBe('Test User')
  })

  it('handles file input change', async () => {
    const file = new File(['dummy content'], 'profile.png', { type: 'image/png' })
    const fileInput = wrapper.find('input[type="file"]')
    await fileInput.trigger('change', { target: { files: [file] } })
    expect(wrapper.vm.profilePicture).toBe(file)
  })

  it('submits form data correctly', async () => {
    axios.post.mockResolvedValue({})

    wrapper.setData({
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      first_name: 'Test',
      last_name: 'User',
      fullName: 'Test User',
      profilePicture: new File(['dummy content'], 'profile.png', { type: 'image/png' }),
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(axios.post).toHaveBeenCalled()
    const formData = axios.post.mock.calls[0][1]
    expect(formData.get('username')).toBe('testuser')
    expect(formData.get('fullName')).toBe('Test User')
    expect(formData.get('profilePicture').name).toBe('profile.png')
  })

  it('displays error message on registration failure', async () => {
    axios.post.mockRejectedValue({
      response: {
        data: {
          email: ['This email is already taken.']
        }
      }
    })

    wrapper.setData({
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      first_name: 'Test',
      last_name: 'User',
      fullName: 'Test User',
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.vm.error).toContain('email: This email is already taken.')
  })
})
