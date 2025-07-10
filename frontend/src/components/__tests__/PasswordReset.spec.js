import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PasswordReset from '../PasswordReset.vue';

describe('PasswordReset.vue', () => {
  it('renders password reset form', () => {
    const wrapper = mount(PasswordReset);
    expect(wrapper.exists()).toBe(true);
  });
});
